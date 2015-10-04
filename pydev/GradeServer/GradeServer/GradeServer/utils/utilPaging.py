# -*- coding: utf-8 -*-

import math 

from GradeServer.resource.otherResources import OtherResources

"""
페이징에 필요한 정보들을 구하는 모듈
"""
def get_page_pointed(pageNum, count, LIST = OtherResources().const.LIST, BLOCK = OtherResources().const.BLOCK):
    
    #Show List
    startList = (pageNum - 1) * LIST
    endList = (pageNum * LIST) if startList + LIST < count - 1 else count

    #show Page
    allPage = int(math.ceil(count / float(LIST)))
    extraPage = BLOCK / 2
    startPage = 1 if pageNum <= extraPage\
                     or allPage <= BLOCK else pageNum - extraPage
    endPage = pageNum if pageNum == allPage else (BLOCK if startPage == 1 else pageNum + extraPage)
    #Minimum Page
    if endPage > allPage:
        endPage = allPage

    return {'LIST': LIST,
            'BLOCK': BLOCK,
            'count': count,
            'pageNum': pageNum,
            'startList': startList,
            'endList': endList,
            'startPage': startPage,
            'endPage': endPage,
            'allPage': allPage}
    
    
'''
Page Number Case Record
'''
def get_page_record(recordsSub, pageNum, LIST = OtherResources().const.LIST):
        
    return recordsSub.slice((pageNum - 1) * LIST,
                            pageNum * LIST)
