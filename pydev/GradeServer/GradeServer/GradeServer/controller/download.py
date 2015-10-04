# -*- coding: utf-8 -*-
"""
    GradeSever.controller.download
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    과목별 파일 다운로드

    :copyright: (c) 2015 by KookminUniv

"""

from flask.helpers import send_from_directory, session

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.resource.sessionResources import SessionResources

from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer


@GradeServer.route('/download_file?')
@login_required
@check_invalid_access
def download_file():
    try:
        # Absolute Path
        directory = '/mnt/shared/Past/'
        # File Name StudentId_MemberName.zip
        filename = session[SessionResources().const.MEMBER_ID] + '_'\
        + session[SessionResources().const.MEMBER_NAME] + '.zip'
        
        Log.info(session[SessionResources().const.MEMBER_ID] \
                 + ' download '\
                 + directory\
                 + '/'  + filename)
        
        return send_from_directory(directory = directory, filename = filename)
    except Exception:
        pass
