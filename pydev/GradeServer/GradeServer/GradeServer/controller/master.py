# -*- coding: utf-8 -*-
'''
    GradeSever.controller.master

    Functions for server administrator
    
    :author: seulgi choi & uijae lee
    :copyright: (c) 2015 by Algorithmic Engineering Lab at KOOKMIN University
'''
import fnmatch, shutil

from flask import request, render_template, session
from sqlalchemy import exc
from datetime import datetime

from werkzeug.security import generate_password_hash

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.parameter.filterFindParameter import FilterFindParameter

from GradeServer.utils.utilSubmissionQuery import insert_submitted_records_of_problems
from GradeServer.utils.utilUserQuery import select_members,\
                                            select_member,\
                                            members_sorted,\
                                            search_members,\
                                            update_member_deleted,\
                                            select_match_member_id,\
                                            insert_members
                                            
from GradeServer.utils.utilProblemQuery import select_problem,\
                                               select_problems,\
                                               insert_problem,\
                                               update_problem_deleted,\
                                               update_problem,\
                                               update_number_of_test_case
                                               
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utils import get_request_value
from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilMessages import unknown_error
from GradeServer.utils.utils import is_authority

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.GradeServer_py3des import TripleDES

from GradeServer.database import dao
from GradeServer.GradeServer_logger import Log
from GradeServer import page_not_found
from GradeServer.GradeServer_blueprint import GradeServer

import re
import zipfile
import os
import subprocess
import glob

projectPath='/mnt/shared'
problemsPath='%s/Problems' % (projectPath) # /mnt/shared/Problems
pyPath='%s/pydev/GradeServer/GradeServer/GradeServer' % (projectPath)
problemDescriptionsPath='%s/static/ProblemDescriptions' % (pyPath)
tmpPath='%s/tmp' % (projectPath)

@GradeServer.teardown_request
def close_db_session(exception = None):
    '''요청이 완료된 후에 db연결에 사용된 세션을 종료함'''
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))
        
        

def handle_file_came_from_window(rowProblemName, decodedProblemName):
    '''
    @@ Make imitation of Original problem name
    
    Original problem name shows with question mark
    To find and change the name to decoded name, make fake temporary name
    '''
    
    # role of fake problem name
    byteString='?'*len(rowProblemName)

    error=change_directory_to(tmpPath)

    if not error:
        if rename_file('%s.txt'%byteString, '%s.txt'%decodedProblemName):
            return error
        
        '''
        @@ Rename PDF file name
        
        PDF file is optional so, doesn't block when error occurs.
        '''
        if rename_file('%s.pdf'%byteString, '%s.pdf'%decodedProblemName):
            return error
                        
        '''
        @@ Rename _SOLUTION or _CHECKER folder name
        
        Figure out its solution check type from folder name
        '''
        currentPath, error=get_current_path()
        if error: return error
        
        filesInCurrentDir=glob.glob(currentPath+'/*')
        solCheckType=None
        for name in filesInCurrentDir:
            if '_SOLUTION' in name:
                solCheckType='SOLUTION'
                break
            if '_CHECKER' in name:
                solCheckType='CHECKER'
                break
            
        if solCheckType:
            originalFolder='%s_%s' % (byteString, solCheckType)
            newFolder='%s_%s' % (decodedProblemName, solCheckType)
            
            if rename_file(originalFolder, newFolder): return error
                
        # If SOLUTION or CHEKER file doesn't exist then it's an error
        else:
            error=LanguagesResources().const.SolutionCheckerDirError
        
    return error


def remove_space_from_names_in(path):
    error=change_directory_to(path)
    
    if not error:
        try:
            subprocess.call('for f in *;do mv "$f" `echo $f|sed "s/ //g"`;done',\
                            shell=True)
        except OSError:
            error=LanguageResources().const.RemoveSpaceError
    
    return error



def get_current_path():
    error=None
    
    try:
        currentPath=os.getcwd()
    except OSError:
        error=LanguageResources().const.GetCurrentDirError

    return currentPath, error                                        


def change_directory_to(path):
    error=None
    
    try:
        os.chdir(path)
    except OSError:
        error=LanguageResources().const.ChangeDirError
    
    return error


def rename_file(fromA, toB):
    error=None
    
    try:
        subprocess.call('mv %s %s' % (fromA, toB), shell=True)
    except OSError:
        error=LanguageResources().const.RenameFileError
    
    return error


def remove_carriage_return(path):
    error = change_directory_to(path)
    if not error:
        try:
            subprocess.call('cp %s/static/shell/remove_crlf.sh ./' % pyPath, shell=True)
        except:
            return LanguageResources().const.MoveShellError
        
        try:
            subprocess.call('sh remove_crlf.sh', shell=True)
            subprocess.call('rm *.sh *.sh+tmp', shell=True)
        except:
            return LanguageResources().const.RemoveShellError
    
    return error


 
'''
show create Problems page
'''   
@GradeServer.route('/manage_problem?page=<int:pageNum>&problemLevel=<problemLevel>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def manage_problem(problemLevel, pageNum, error = None):
    try:
        # Upload Problems Files
        if request.method == 'POST':
            if is_authority(session[SessionResources().const.AUTHORITY])[0]:
                error = post_problem(request)
            else:
                error = LanguageResources().const.GetOutHere
        
        # GET, POST 공통 사항
        problems = select_problems(None if problemLevel == LanguageResources().const.All[1]
                                   else problemLevel)
        
        try:
            count = select_count(problems.subquery().c.problemIndex).first().\
                                                          count
            
            problemRecords = get_page_record(problems,
                                             pageNum = pageNum).all()
            
        except Exception:
            count = 0 
            problemRecords = []
        
        return render_template('/manage_problem.html', 
                               types = [ENUMResources().const.SOLUTION,
                                        ENUMResources().const.CHECKER],
                               levels = [LanguageResources().const.GoldLevel,
                                         LanguageResources().const.SilverLevel,
                                         LanguageResources().const.BronzeLevel],
                               problemLevel = problemLevel,
                               problemRecords = problemRecords,
                               pages = get_page_pointed(pageNum,
                                                        count),
                               error = error)
    except Exception as e:
        return unknown_error(e)
    

'''
members add, modify, delete function supply

filterCondition and keyWord is Search Event
'''
@GradeServer.route('/manage_user?filterCondition=<filterCondition>&keyWord=<keyWord>&page=<int:pageNum>&sortCondition=<sortCondition>',methods=['GET','POST'])
@login_required
@check_invalid_access
def manage_user(filterCondition, keyWord, sortCondition, pageNum, error = None):
    # Not Accept URL Check
    
    if sortCondition not in (LanguageResources().const.ID[1],
                                LanguageResources().const.Name[1]):
        return page_not_found()
    
    try:
        # Request Post
        if request.method == 'POST':
            # Search Event
            # FilterCondition
            if len(request.form) <= 2 and 'keyWord' in request.form:
                for form in request.form:
                    if 'keyWord' != form:
                        filterCondition = form
                        keyWord = get_request_value(form = request.form,
                                                    name = 'keyWord')
                        pageNum = 1
                        
                        break
            elif is_authority(session[SessionResources().const.AUTHORITY])[0]:
                if 'memberDeleted' in request.form:
                    for form in request.form:
                        if 'member' not in form and 'keyWord' not in form:
                            memberIdIndex = form
                            # Get Folder Path
                            member = select_member(memberIdIndex = memberIdIndex).first()
                            
                            try:
                                update_member_deleted(memberIdIndex)
                                dao.commit()
                                
                                userPath = '{0}/Current/{1}_{2}'.format(projectPath,
                                                                        member.memberId,
                                                                        member.memberName)
                                # Delete Folder
                                if os.path.exists(userPath):
                                    shutil.rmtree(userPath)
                            except Exception:
                                dao.rollback()
                                error = LanguageResources().const.DBFailed
                else:
                    for form in request.form:
                        # Insert Indivisual
                        if 'memberInsert' in form:
                            insertCount = int(form[len('memberInsert'):]) + 1
                           
                            for i in range(1, insertCount):
                                # Get Input Data
                                detailInformation = get_request_value(form = request.form,
                                                                      name = 'detailInformation{0}'.format(i))
                                memberId = get_request_value(form = request.form,
                                                             name = 'memberId{0}'.format(i))
                                memberName = get_request_value(form = request.form,
                                                               name = 'memberName{0}'.format(i))
                               
                                if memberId\
                                   and memberName:
                                    try:
                                        memberIdIndex = select_match_member_id(memberId).first().\
                                                                                         memberIdIndex
                                    except Exception:
                                        memberIdIndex = None
                                    try:
                                        error = insert_member_registration(memberIdIndex = memberIdIndex,
                                                                           memberId = memberId,
                                                                           memberName = memberName,
                                                                           password = generate_password_hash(TripleDES.encrypt(str(memberId))),
                                                                           detailInformation = detailInformation)
                                        dao.commit()
                                        
                                        # Get Folder Path
                                        userPath = '{0}/Current/{1}_{2}'.format(projectPath,
                                                                                memberId,
                                                                                memberName)
                                        # make Folders
                                        if not os.path.exists(userPath):
                                            os.makedirs(userPath)
                                    except Exception:
                                        dao.rollback()
                                        error = LanguageResources().const.DBFailed
                                else:
                                    error = LanguageResources().const.FormValidation
            else:
                error = LanguageResources().const.GetOutHere
                
        # Get Users
        try:
            members = select_members().subquery()
            # Filter Case
            if filterCondition\
               and filterCondition != ' ':
                if not keyWord:
                    keyWord = ' '
                members = search_members(members,
                                         FilterFindParameter(filterCondition = filterCondition,
                                                             keyWord = (keyWord if keyWord != ' '
                                                                        else ''))).subquery()
            count = select_count(members.c.memberIdIndex).first().\
                                                          count
            memberRecords = get_page_record(members_sorted(members,
                                                           sortCondition),
                                            pageNum = pageNum)
        except Exception:
            count = 0 
            memberRecords = []
            
        return render_template('/manage_user.html',
                               # 검색시 FilterCondition List
                               Filters = [LanguageResources().const.All,
                                          LanguageResources().const.ID,
                                          LanguageResources().const.Name],
                               sortCondition = sortCondition,
                               filterCondition = filterCondition,
                               keyWord = keyWord,
                               memberRecords= memberRecords,
                               pages = get_page_pointed(pageNum,
                                                        count),
                               count = count,
                               error = error)
    except Exception as e:
        return unknown_error(e)

def insert_member_registration(memberIdIndex, memberId, memberName, password, detailInformation, error = None):
    if memberIdIndex:
        # Duplication Registrations
        error = LanguageResources().const.Exist
    else:
        dao.add(insert_members(memberId = memberId,
                               memberName = memberName,
                               password = password,
                               signedInDate = datetime.now(),
                               detailInformation = detailInformation))
            
    return error  



@GradeServer.route('/manage_service')
@login_required
@check_invalid_access
def server_manage_service():   
    #TODO     
    error=None
    
    return render_template('/server_manage_service.html',
                           error=error)



def post_problem(request, error = None):
    if 'upload' in request.form:
        files = request.files.getlist('files')
        # Get Fle Failed
        if not list(files)[0].filename:
            return LanguageResources().const.UploadingFileError

        # read each uploaded file(zip)
        for fileData in files:
            # create temporary path to store new problem before moving into 'Problems' folder
            tmpPath='%s/tmp' % projectPath
            
            '''
            @@ Check and Delete temporary folder
            
            If temporary folder 'tmp' is exist, then it means it had an error at past request.
            So, remove the temporary folder 'tmp' first.
            '''
            if os.path.exists(tmpPath):
                try:
                    subprocess.call('rm -rf %s' % tmpPath,
                                    shell = True)
                except OSError:
                    return LanguageResources().const.DeleteFolderError
            
            # unzip file
            with zipfile.ZipFile(fileData,
                                 'r') as z:
                z.extractall(tmpPath)
            
            try:
                rowProblemName = re.split('_|\.',
                                          os.listdir(tmpPath)[0])[0].\
                                             replace(' ', '\ ')
            except OSError:
                return LangaugeResources().const.ListingFilesError
            '''
            @@ Decode problem name
            
            If the problem zip's made on window environment, problem name's broken
            So it needs to be decoded by cp949
            ''' 
            problemName = str(rowProblemName.decode('cp949'))
            # if decoded name is the same with before decoding, 
            # it means the file is not created on window environment
            isFromWindow = True if rowProblemName != problemName\
                           else False
            
            if isFromWindow:
                error = handle_file_came_from_window(rowProblemName, problemName)
                if error: return error
            
            problemInformationPath = ('%s/%s.txt' %(tmpPath,
                                                    problemName)).replace('\ ', ' ')
            try:
                # 'open' command can handle space character without '\' mark,
                # Replace '\ ' to just space ' '
                problemInfoFile = open(problemInformationPath, 'r')
                problemInformation = problemInfoFile.read()
                
                try:
                    problemInfoFile.close()
                except IOError:
                    return LanguageResources().const.ClosingFileError
                    
            except IOError:
                return LanguageResources().const.ReadingFileError

            '''
            @@ Decode problem meta information
            
            Problem meta information(.txt) file needs to be decoded as well as problem folder name
            '''
            if isFromWindow:
                problemInformation = problemInformation.decode('cp949')
            # slice and make key, value pairs from csv form
            problemInformation = problemInformation.replace(' ', '').split(',')
            # re-slice and make information from 'key=value'
            for eachInformation in problemInformation:
                key, value = eachInformation.split('=')
                if key == 'Name':
                    # 'value' doesn't have a space character because of 'replace(' ', '')' command above
                    # Don't use 'value' for problem name
                    problemName = problemName.replace('\ ', ' ')
                elif key == 'Difficulty':
                    if isinstance(value, int):
                        problemDifficulty = int(value)
                    else:
                        return LanguageResources().const.DifficultyCharError
                elif key == 'SolutionCheckType':
                    solutionCheckType = ENUMResources().const.SOLUTION if value == 'Solution'\
                                        else ENUMResources().const.CHECKER
                elif key == 'LimitedTime':
                    limitedTime = int(value)
                elif key == 'LimitedMemory':
                    limitedMemory = int(value)
            # Insert new problem
            problemPath = '%s/%s' % (problemsPath,
                                     problemName.replace(' ', ''))
            if not select_problem(problemIndex = None,
                                  problemName = problemName,
                                  isDeleted = ENUMResources().const.TRUE).first():
                dao.add(insert_problem(problemName,
                                       problemDifficulty,
                                       solutionCheckType,
                                       limitedTime,
                                       limitedMemory,
                                       problemPath))
            else:
                # Duplication Case
                update_problem_deleted(select_problem(problemIndex = None,
                                                      problemName = problemName,
                                                      isDeleted = ENUMResources().const.TRUE).first().\
                                                                                 problemIndex,
                                       isDeleted = ENUMResources().const.FALSE)
           
            newProblemPath='%s/%s_%s' %\
                           (tmpPath, problemName, solutionCheckType)
            if change_directory_to(newProblemPath): return
                                
            try:
                # current path : ../tmp/problemName_solutionCheckType
                inOutCases=\
                    [filename for filename in os.listdir(os.getcwd())]
            except OSError:
                return LanguageResources().const.ListingFilesError

            for filename in inOutCases:
                rowFileName=filename
                fileName='%s_%s' %\
                         (problemName, rowFileName.split('_', 1)[1])
        
                if rename_file(rowFileName, str(fileName)): return

            '''
            @@ Changing directory/file name
            
            work flow
            1. Remove space on its name
                from> Hello World 
                to> HelloWorld
                
            2. Attach problem ID ahead of the name
                from> HelloWorld
                to> 12345_HelloWorld
                * 12345 is created problem id
            '''
            currentPath, error=get_current_path()
            if error: return error

            # inside of SOLUTION or CHECKER folder
            error = remove_space_from_names_in(currentPath)
            if error: return error
            
            # move to outside of the folder
            if change_directory_to(tmpPath): return error
            
            currentPath, error=get_current_path()
            if error: return error
            
            # inside of Problem folder
            error = remove_space_from_names_in(currentPath)
            if error: return error
            
            # create final goal path
            if not os.path.exists(problemPath):
                os.makedirs(problemPath)

            problemName = problemName.replace(' ', '')
            problemDescriptionPath = '%s/%s' %(problemDescriptionsPath,
                                               problemName)
            if not os.path.exists(problemDescriptionPath):
                os.makedirs(problemDescriptionPath)

            error = rename_file('%s/*'%tmpPath, '%s/'%problemPath)
            if error: return error

            try:
                subprocess.call('cp %s/%s.pdf %s/' %\
                                (problemPath, problemName,\
                                problemDescriptionPath), shell=True)
            except:
                return LanguageResources().const.NotExistPDF

            error = remove_carriage_return(problemPath+'/'+problemName+'_'+solutionCheckType)
            if error: return error
            
    
    # Modify or Deleted Case
    else:
        if 'problemModify' in request.form:
            # Seach ProblemIndex
            updateProblemCount, updateCount = len(request.form) / 5, 0 
            
            for form in request.form:
                if updateProblemCount == updateCount:
                    break
                elif 'problem' not in form\
                      and 'limited' not in form:
                    updateCount = updateCount + 1
                    update_problem(problemIndex = form,
                                   problemDifficulty = request.form['problemDifficulty' + form],
                                   solutionCheckType = request.form['problemType' + form],
                                   limitedTime = request.form['limitedTime' + form],
                                   limitedMemory = request.form['limitedMemory' + form])
        elif 'problemDeleted' in request.form:
            # Get ProblemIndex
            for form in request.form:
                if 'problem' not in form:
                    update_problem_deleted(problemIndex = form)
    
    try:
        dao.commit()
        if 'upload' in request.form:
            # update numberOfTestCase
            problem = select_problem(problemIndex = None,
                                     problemName = problemName).first()
            testCasePath = '{0}/Problems/{1}/{2}_SOLUTION/'.format(projectPath, 
                                                                   problem.problemName, 
                                                                   problem.problemName) 
    
            numberOfTestCase = len(fnmatch.filter(os.listdir(testCasePath), '*.txt')) / 2
            update_number_of_test_case(problem.problemIndex,
                                       numberOfTestCase)
            
            try:
                dao.add(insert_submitted_records_of_problems(problem.problemIndex))
                
                dao.commit()
            except Exception:
                dao.rollback() 
        elif 'problemDeleted' in request.form:
            # Get ProblemIndex
            for form in request.form:
                if 'problem' not in form:
                    # Delete Folder
                    problem = select_problem(int(form),
                                             isDeleted = ENUMResources().const.TRUE).first()
                    problemPath = '{0}/Problems/{1}/'.format(projectPath,
                                                             problem.problemName)
                    if os.path.exists(problemPath):
                        shutil.rmtree(problemPath)

    except exc.SQLAlchemyError:
        dao.rollback()
        error = LanguageResources().const.DBFailed
            
    return error
