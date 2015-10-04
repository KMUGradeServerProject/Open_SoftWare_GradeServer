# -*- coding: utf-8 -*-
"""
    GradeSever_config
    ~~~~~~~~

    :copyright: (c) 2015 by Algorithmic Engineering Lab.
"""


class GradeServerConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'mysql+mysqlconnector://{0}:{1}@localhost/GradeServer'
    #: 사진 업로드 시 사진이 임시로 저장되는 임시 폴더
    TMP_FOLDER = 'resource/tmp/'
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    # 업로드 파일 경로
    UPLOAD_FOLDER = '/mnt/shared/Temp'
    CURRENT_FOLDER = '/mnt/shared/Current'
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'GradeServer_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    


