# -*- coding: utf-8 -*-
import os
import sys
import logging
from grading import InterfaceGrade
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # 명령행 인수 리스트로 저장
    args = sys.argv
    
    # 명령행 인수 개수가 맞지 않는 경우
    if len(args) is not 11:
        sys.stderr.write(ENUMResources.const.SERVER_ERROR + ' ' + str(0) + ' ' + str(0) + ' ' + str(0))
        sys.exit()
    
    logging.debug(args[3] + ' grading start')
    
    # host와 연결된 디렉토리로 이동
    os.chdir(FileNameNPathResources.const.TempDirectory)

    # 인터페이스 객체 생성
    grade = InterfaceGrade.InterfaceGrade(args)
    
    # 코드 컴파일
    result = grade.compile()
    
    # 실행 및 채점
    result, score, runTime, usingMem = grade.evaluation()
