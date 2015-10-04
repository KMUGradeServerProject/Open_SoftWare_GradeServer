#-*- coding: utf-8 -*-

import os, time

from flask import request, redirect, url_for, session, flash
from werkzeug import secure_filename

from GradeServer.database import dao
from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer
from GradeServer.utils.loginRequired import login_required
from GradeServer.GradeServer_config import GradeServerConfig
from GradeServer.utils.utilCodeSubmissionQuery import get_member_name,\
                                                      get_problem_name,\
                                                      get_submission_info,\
                                                      insert_submitted_files,\
                                                      get_submission_index,\
                                                      get_used_language_index,\
                                                      insert_to_submissions,\
                                                      get_problem_info,\
                                                      delete_submitted_files_data
from GradeServer.utils.utilMessages import get_message
from GradeServer.utils.checkInvalidAccess import check_invalid_access
from GradeServer.utils.utils import get_request_value

from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.tasks import Grade

# PATH = '/mnt/shared/CurrentCourses'
PATH = GradeServerConfig.CURRENT_FOLDER

# remove space in problemName
def remove_space_in_problemName(problemIndex):
    problemName = get_problem_name(problemIndex)
    return problemName.replace(' ', '')

# make file save paths
def make_path(PATH, memberIdIndex, memberId, problemName):
    memberName = get_member_name(memberIdIndex)
    filePath = OtherResources().const.FILE_PATH %(PATH, memberId, memberName, problemName)
    tempPath = OtherResources().const.TEMP_PATH %(PATH, memberId, memberName, problemName)
    return filePath.replace(' ', ''), tempPath.replace(' ', '')

# file save when file uploaded
def file_save(submissionIndex, uploadFiles, tempPath, filePath):
    fileIndex = 1
    sumOfSubmittedFileSize = 0
    delete_submitted_files_data(submissionIndex)
    for file in uploadFiles:
        fileName = secure_filename(file.filename)
        if len(file.filename) != len(fileName):
            fileName = file.filename.decode()
        file.save(os.path.join(tempPath, fileName))
        fileSize = os.stat(os.path.join(tempPath, fileName)).st_size
        insert_submitted_files(submissionIndex, fileIndex, fileName, filePath, fileSize)
        fileIndex += 1
        sumOfSubmittedFileSize += fileSize
        
    return sumOfSubmittedFileSize
        
# send to celery function
# member's info, course info, problem info, language info, file info etc..       
def send_to_celery(memberIdIndex, problemIndex, submissionIndex, usedLanguageName, usedLanguageVersion, sumOfSubmittedFileSize, problemName, filePath, tempPath):
    if usedLanguageName == OtherResources().const.PYTHON:
        usedLanguageIndex = get_used_language_index(usedLanguageName, usedLanguageVersion)
    else:
        usedLanguageIndex = get_used_language_index(usedLanguageName)
    submissionCount, solutionCheckCount = get_submission_info(memberIdIndex, problemIndex)
    insert_to_submissions(submissionIndex, submissionCount, solutionCheckCount, usedLanguageIndex, sumOfSubmittedFileSize)
    problemPath, limitedTime, limitedMemory, solutionCheckType, numberOfTestCase = get_problem_info(problemIndex, problemName)
    
    if numberOfTestCase >= 2:
        numberOfTestCase -= 1
            
    Grade.delay(submissionIndex,
                submissionCount,
                int(problemIndex),
                str(filePath),
                str(problemPath),
                str(solutionCheckType),
                numberOfTestCase,
                limitedTime,
                limitedMemory,
                str(usedLanguageName),
                str(usedLanguageVersion),
                str(problemName))
    
    dao.commit()
    
    flash(LanguageResources().const.SubmissionSuccess[session[OtherResources().const.LANGUAGE]])
    os.system(OtherResources().const.DELETE_COMMAND % filePath)
    os.rename(tempPath, filePath)
    
# get language name from html tag
def get_language_name(usedLanguageName):
    if usedLanguageName == OtherResources().const.C:
        languageName = OtherResources().const.C_SOURCE_NAME

    if usedLanguageName == OtherResources().const.CPP:
        languageName = OtherResources().const.CPP_SOURCE_NAME

    if usedLanguageName == OtherResources().const.JAVA:
        languageName = OtherResources().const.JAVA_SOURCE_NAME

    if usedLanguageName == OtherResources().const.PYTHON:
        languageName = OtherResources().const.PYTHON_SOURCE_NAME

    return languageName

# write code save function
def write_code_in_file(tempPath):
    tests = request.form[OtherResources().const.GET_CODE]
    unicode(tests)
    tests = tests.replace(OtherResources().const.LINUX_NEW_LINE, OtherResources().const.WINDOWS_NEW_LINE)
    usedLanguageName = get_request_value(request.form,
                                         OtherResources().const.LANGUAGE)
    usedLanguageVersion = None
    if usedLanguageName == OtherResources().const.PYTHON2:
        usedLanguageName = OtherResources().const.PYTHON
        usedLanguageVersion = OtherResources().const.PYTHON2_VERSION
    elif usedLanguageName == OtherResources().const.PYTHON3:
        usedLanguageName = OtherResources().const.PYTHON
        usedLanguageVersion = OtherResources().const.PYTHON3_VERSION
    
    fileName = get_language_name(usedLanguageName)
    fout = open(os.path.join(tempPath, fileName), 'w')
    fout.write(tests)
    fout.close()

    return usedLanguageName, usedLanguageVersion, fileName

# page move function when problem submitted
def page_move(pageNum, browserName = None, browserVersion = None):
    if (browserName == OtherResources().const.EXPLORER and len(browserVersion) != 4) or browserName == None:
        return redirect(url_for(RouteResources().const.PROBLEM_LIST,
                                pageNum = pageNum))
    return "0"

# error print function when error occured
def submit_error(tempPath, pageNum, error, browserName = None, browserVersion = None):
    os.system(OtherResources().const.DELETE_COMMAND % tempPath)
    flash(get_message(error))
    return page_move(pageNum, browserName, browserVersion)

# uploaded files processing function
# make file save folder, submitted file information insert to DB etc..
@GradeServer.route('/problem_<problemIndex>_<pageNum>_<browserName>_<browserVersion>', methods = ['POST'])
@check_invalid_access
@login_required
def to_process_uploaded_files(problemIndex, pageNum, browserName, browserVersion):
    memberId = session[SessionResources().const.MEMBER_ID]
    memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]
    problemName = remove_space_in_problemName(problemIndex)
    filePath, tempPath = make_path(PATH, memberIdIndex, memberId, problemName)

    try:
        os.mkdir(tempPath)
        uploadFiles = request.files.getlist(OtherResources().const.GET_FILES)
        usedLanguageName = request.form[OtherResources().const.USED_LANGUAGE_NAME]
        usedLanguageVersion = request.form[OtherResources().const.USED_LANGUAGE_VERSION]
        submissionIndex = get_submission_index(memberIdIndex, problemIndex)
        sumOfSubmittedFileSize = file_save(submissionIndex, uploadFiles, tempPath, filePath)
        send_to_celery(memberIdIndex, problemIndex, submissionIndex, usedLanguageName, usedLanguageVersion, sumOfSubmittedFileSize, problemName, filePath, tempPath)
        Log.info(OtherResources().const.FILE_SUBMITTED)
    except OSError as e:
        Log.error(str(e))
        submit_error(tempPath, pageNum, OtherResources().const.FILE_ERROR, browserName, browserVersion)
    except Exception as e:
        dao.rollback()
        Log.error(str(e))
        print e
        submit_error(tempPath, pageNum, OtherResources().const.DB_ERROR, browserName, browserVersion)
        
    time.sleep(0.4)
    
    return page_move(pageNum, browserName, browserVersion)
    
# write code processing function
#  make file save folder, submitted file information insert to DB etc..    
@GradeServer.route('/problem_page<pageNum>_<problemIndex>', methods = ['POST'])
@check_invalid_access
@login_required
def to_process_written_code(pageNum, problemIndex):
    memberId = session[SessionResources().const.MEMBER_ID]
    memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]
    problemName = remove_space_in_problemName(problemIndex)
    filePath, tempPath = make_path(PATH, memberIdIndex, memberId, problemName)
    try:
        os.mkdir(tempPath)
        usedLanguageName, usedLanguageVersion, fileName = write_code_in_file(tempPath)
        fileSize = os.stat(os.path.join(tempPath, fileName)).st_size
        fileIndex = 1
        submissionIndex = get_submission_index(memberIdIndex, problemIndex)
        delete_submitted_files_data(submissionIndex)
        insert_submitted_files(submissionIndex, fileIndex, fileName, filePath, fileSize)
        send_to_celery(memberIdIndex, problemIndex, submissionIndex, usedLanguageName, usedLanguageVersion, fileSize, problemName, filePath, tempPath)
        Log.info(OtherResources().const.WRITED_CODE_SUBMITTED)
    except OSError as e:
        Log.error(str(e))
        submit_error(tempPath, pageNum, OtherResources().const.FILE_ERROR)
    except Exception as e:
        dao.rollback()
        Log.error(str(e))
        print e
        submit_error(tempPath, pageNum, OtherResources().const.DB_ERROR)
        
    time.sleep(0.4)
    
    return page_move(pageNum)
