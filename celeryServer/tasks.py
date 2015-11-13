from __future__ import absolute_import
from celeryServer import app

import os
import time
import DBUpdate
from DBManager import db_session
from subprocess import Popen, PIPE, call
from billiard import current_process

MAX_CONTAINER_COUNT = 1

def Restart(number):
    call('sudo docker stop grade_container' + number, shell = True)
    call('sudo docker rm grade_container' + number, shell = True)

    containerCreadeCommand = "%s%i%s%i %s" %('sudo docker create --privileged -i -t --name --cpuset="',
                                              number, '" grade_container', number,
                                              'gradeserver:1.0 /bin/bash')
        
    runProgramInContainer = '%s%i %s' % ('sudo docker exec grade_container',
                                          number, 'python -B /gradeprogram/*')
    call(containerCreadeCommand, shell = True)
    call('sudo docker start grade_container' + number, shell = True)
    call(runProgramInContainer, shell = True)

class SqlAlchemyTask(app.Task):
    abstract = True
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()
    

@app.task(name = 'task.Grade', base=SqlAlchemyTask)
def Grade(submissionIndex, submissionCount, problemIndex, filePath,
          problemPath, gradeMethod, caseCount, limitTime, limitMemory, usingLang,
          version, problemName):
    worker_num = current_process().index % MAX_CONTAINER_COUNT + 1
    
    saveDirectoryName = "%i_%i" % (submissionIndex, submissionCount)
    
    sharingDirName = "/mnt/shared/tempdir/%s" % (saveDirectoryName)
    
    argsList = "%s %s %s %s %i %i %i %s %s %s" % (filePath, problemPath,
                                                  saveDirectoryName, gradeMethod,
                                                  caseCount, limitTime,
                                                  limitMemory, usingLang,
                                                  version, problemName)
    
    containerCommand = "%s%i %s" % ('sudo docker exec grade_container', worker_num,
                                   'python /gradeprogram/rungrade.py ')
    
    print 'program start'
    
    try:
        call(containerCommand + argsList, shell=True)
        UpdateResult(submissionIndex, submissionCount, problemIndex, sharingDirName)
    except Exception as e:
        print e
        UpdateResult(submissionIndex, submissionCount, problemIndex)
        Restart(worker_num)
        
def UpdateResult(submissionIndex, submissionCount,
                 problemIndex, sharingDirName = None):        
    dataUpdate = DBUpdate.DBUpdate(submissionIndex, submissionCount, problemIndex)
    
    if sharingDirName is None:
        dataUpdate.UpdateServerError(submissionIndex, submissionCount, db_session)
   
    dirPath = sharingDirName + "/message.txt"
    try:
        if (not os.path.isfile(dirPath)) or os.path.getsize(dirPath) is 0:
            text = '0'
        
        else:
            fp = open(sharingDirName + '/message.txt', 'r')
            text = fp.read()
            fp.close()
    
    except Exception:
        dataUpdate.UpdateServerError(submissionIndex, submissionCount, db_session)
        return
        
    fp = open(sharingDirName + '/container.txt')
    messageLine = fp.readlines()[-1]
    messageParaList = messageLine.split()
        
    result = dataUpdate.UpdateResutl(messageParaList, db_session, text)
    
    if not result:
        dataUpdate.UpdateServerError(submissionIndex, submissionCount, db_session)
