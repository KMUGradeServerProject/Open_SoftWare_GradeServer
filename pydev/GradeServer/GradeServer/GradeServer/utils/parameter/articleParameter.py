# -*- coding: utf-8 -*-
"""
    GradeServer.utils
    ~~~~~~~~~~~~~~

    GradeSever에 적용될 ArticleParameter 대한 패키지 초기화 모듈.

    :copyright: (c) 2015 kookminUniv
    :@author: algolab
"""
    
class ArticleParameter:
    # Article type contents
    title = None
    content = None
    updateIp = None
    updateDate = None
    
    def __init__(self, title = None, content = None, updateIp = None, updateDate = None):
        self.title = title
        self.content = content
        self.updateIp = updateIp
        self.updateDate = updateDate
