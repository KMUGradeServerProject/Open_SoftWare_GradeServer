

class OtherResources(object):
    """Other Resource Static Class"""
    
    from GradeServer.resource import const
    
    # key 
    const.TRIPLE_DES_KEY = '1234567812345678'
    # Integer
    const.LIMIT_TITLE_VIEW_LENGTH = 25
    const.TITLE_VIEW_LENGTH = 22
    const.NOTICE_LIST = 5
    const.BLOCK = 11
    const.LIST = 25
    const.VIEW_NOTICE = 5
    # Pixel
    const.TEXTAREA_ROW = 400
    const.MAX_ROW = 700
    const.REPLY_ROW = 50

    # file
    const.PDF_PATH = '/mnt/shared/pydev/GradeServer/GradeServer/GradeServer/static/ProblemDescriptions/%s/%s.pdf'
    const.FILE_PATH = '%s/%s_%s/%s'
    const.TEMP_PATH = '%s/%s_%s/%s_tmp'
    const.GET_FILES = 'file[]'
    const.DELETE_COMMAND = 'rm -rf %s'
    const.USED_LANGUAGE_NAME = 'usedLanguageName'
    const.USED_LANGUAGE_VERSION = 'usedLanguageVersion'
    const.GET_CODE = 'getCode'
    const.LANGUAGE = 'language'
    const.C = 'C'
    const.CPP = 'C++'
    const.JAVA = 'JAVA'
    const.PYTHON = 'PYTHON'
    const.PYTHON2 = 'PYTHON2'
    const.PYTHON3 = 'PYTHON3'
    const.PYTHON2_VERSION = '2.7'
    const.PYTHON3_VERSION = '3.4'
    const.EXPLORER = 'msie'
    const.C_SOURCE_NAME = 'main.c'
    const.CPP_SOURCE_NAME = 'main.cpp'
    const.JAVA_SOURCE_NAME = 'main.java'
    const.MISS_CLASS_NAME = 'missClassName.java'
    const.PYTHON_SOURCE_NAME = 'main.py'
    const.JAVA_MAIN_CLASS = r'public\s+class\s+(\w+)'
    const.LINUX_NEW_LINE = '\r\n'
    const.WINDOWS_NEW_LINE = '\n'
    const.SUBMISSION_COUNT = 'submissionCount'
    const.SOLUTION_CHECK_COUNT = 'solutionCheckCount'
    const.VIEW_COUNT = 'viewCount'
    const.FILE_ERROR = 'fileError'
    const.DB_ERROR = 'dbError'
    const.FILE_SUBMITTED = 'file submitted'
    const.WRITED_CODE_SUBMITTED = 'writed code is submitted'
