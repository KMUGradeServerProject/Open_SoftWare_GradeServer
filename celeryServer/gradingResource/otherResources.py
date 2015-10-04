

class OtherResources(object):
    """Other Resource Static Class"""
    
    from gradingResource import const
    
    # key 
    const.TRIPLE_DES_KEY = '1234567812345678'
    # Integer
    const.NOTICE_LIST = 5
    const.BLOCK = 11
    const.LIST = 25

    # file
    const.PDF_PATH = '/mnt/shared/pydev/GradeSever/GradeServer/GradeServer/static/ProblemDescriptions/%s_%s/%s_%s.pdf'
    const.GET_FILES = 'file[]'
    const.USED_LANGUAGE_NAME = 'usedLanguageName'
    const.GET_CODE = 'getCode'
    const.LANGUAGE = 'language'
    const.C = 'C'
    const.CPP = 'C++'
    const.JAVA = 'JAVA'
    const.PYTHON = 'PYTHON'
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
