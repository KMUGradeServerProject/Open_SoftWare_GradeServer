# -*- coding: utf-8 -*-
"""
    runserver
    ~~~~~~~~~

    Tornado Test

    :copyright: (c) 2015 by KookminUniv
    :license: MIT LICENSE 1.0, see license for more details.
"""

import sys
import os

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from GradeServer import create_app

reload(sys).setdefaultencoding('utf-8')

application = create_app(sys.argv)

if __name__ == '__main__':
    
    print 'running...'
    print 'close server : Ctrl + C'
    http_server = HTTPServer (WSGIContainer (application))
    http_server.bind(80)
    http_server.start(1)

    try:
        IOLoop.instance().start ()
    except (KeyboardInterrupt, SystemExit):
        os.system('killall celery')
        
        print 'container stop&rm'
        os.system('docker stop grade_container1')
        os.system('docker rm grade_container1')

        print 'closed server'
    
