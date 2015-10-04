
# -*- coding: utf-8 -*-

from sqlalchemy import or_, and_

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.model.articlesOnBoard import ArticlesOnBoard
from GradeServer.model.likesOnBoard import LikesOnBoard
from GradeServer.model.repliesOnBoard import RepliesOnBoard
from GradeServer.model.likesOnReplyOfBoard import LikesOnReplyOfBoard

from GradeServer.database import dao


'''
Board Articles
'''
def select_articles(isDeleted = ENUMResources().const.FALSE):
    
    return dao.query(ArticlesOnBoard).\
           filter(ArticlesOnBoard.isDeleted == isDeleted)
        
 
'''
Board Article
'''
def select_article(articleIndex, isDeleted = ENUMResources().const.FALSE):   
    return dao.query(ArticlesOnBoard).\
               filter(ArticlesOnBoard.articleIndex == articleIndex,
                      ArticlesOnBoard.isDeleted == isDeleted)
               
                              
'''
Board Notice Classification
'''
def select_sorted_articles(articlesOnBoard, filterFindParameter = None, articleType = ENUMResources().const.NOTICE, isAll = False):
    if articleType == ENUMResources().const.NOTICE:
        # All Notice get
        if isAll:
            articlesOnBoard = dao.query(articlesOnBoard).\
                              filter(articlesOnBoard.c.articleType == ENUMResources().const.NOTICE).\
                              subquery()
            # Filter Case
            if filterFindParameter\
               and filterFindParameter.filterCondition\
               and filterFindParameter.filterCondition != ' ':
                articlesOnBoard = search_articles(articlesOnBoard,
                                                  filterFindParameter).subquery()
        # 5 Get notice
        else:
            # Server written notice get 2
            notice = dao.query(articlesOnBoard).\
                         filter(articlesOnBoard.c.articleType == articleType).\
                         order_by(articlesOnBoard.c.updateDate.desc()).\
                         limit(OtherResources().const.VIEW_NOTICE)
            
            return notice
    else:
        articlesOnBoard = dao.query(articlesOnBoard).\
                              filter(articlesOnBoard.c.articleType != ENUMResources().const.NOTICE).\
                              subquery()
        # Filter Case
        if filterFindParameter\
           and filterFindParameter.filterCondition\
           and filterFindParameter.filterCondition != ' ':
            articlesOnBoard = search_articles(articlesOnBoard,
                                              filterFindParameter).subquery()
        
    return dao.query(articlesOnBoard).\
               order_by(articlesOnBoard.c.articleIndex.desc())
               
               
'''
게시판 검색
'''
def search_articles(articlesOnBoard, filterFindParameter):
    # condition은 All, Id, Title&Content로 나누어서 검새
    if filterFindParameter.filterCondition == LanguageResources().const.All[1]: # Filters[0] is '모두'
        articlesOnBoard = dao.query(articlesOnBoard).\
                             filter(or_(articlesOnBoard.c.memberId == filterFindParameter.keyWord, 
                                        articlesOnBoard.c.title.like('%' + filterFindParameter.keyWord + '%'),
                                        articlesOnBoard.c.content.like('%' + filterFindParameter.keyWord + '%'),
                                        articlesOnBoard.c.problemName.like('%' +filterFindParameter.keyWord + '%')))
    elif filterFindParameter.filterCondition == LanguageResources().const.Writer[1]: # Filters[1] is '작성자'
        articlesOnBoard = dao.query(articlesOnBoard).\
                              filter(articlesOnBoard.c.memberId == filterFindParameter.keyWord)
    elif filterFindParameter.filterCondition == LanguageResources().const.Title[1]: # Filters[2] is '제목&내용'
        articlesOnBoard = dao.query(articlesOnBoard).\
                              filter(or_(articlesOnBoard.c.title.like('% '+ filterFindParameter.keyWord + '%'), 
                                         articlesOnBoard.c.content.like('%' + filterFindParameter.keyWord + '%'),
                                         articlesOnBoard.c.problemName.like('%' +filterFindParameter.keyWord + '%')))

    return articlesOnBoard
                       


'''
Article View Counting
'''
def update_view_reply_counting(articleIndex, VIEW_INCREASE = 1, REPLY_INCREASE = 0):
    dao.query(ArticlesOnBoard).\
        filter(ArticlesOnBoard.articleIndex == articleIndex).\
        update(dict(viewCount = ArticlesOnBoard.viewCount + VIEW_INCREASE,
                    replyCount = ArticlesOnBoard.replyCount + REPLY_INCREASE))
            
 
            
'''
 Board IsLike
'''
def select_article_is_like(articleIndex, memberIdIndex):
    return dao.query(LikesOnBoard).\
               filter(and_(LikesOnBoard.articleIndex == articleIndex,
                           LikesOnBoard.boardLikerIdIndex == memberIdIndex))
               

'''
Insert Articles
'''
def insert_articles_on_board(problemIndex, memberIdIndex, articleType, articleParameter):
    return ArticlesOnBoard(problemIndex = problemIndex,
                           writerIdIndex = memberIdIndex,
                           articleType = articleType,
                           title = articleParameter.title,
                           content = articleParameter.content,
                           updateDate = articleParameter.updateDate,
                           updateIp = articleParameter.updateIp)
    
'''
Insert Article likes
'''
def insert_likes_on_board(articleIndex, memberIdIndex):
    return LikesOnBoard(articleIndex = articleIndex,
                        boardLikerIdIndex = memberIdIndex)
    


''' 
Insert Replies on Board
'''
def insert_replies_on_board(articleIndex, memberIdIndex, articleParameter):
    return RepliesOnBoard(articleIndex = articleIndex,
                          boardReplierIdIndex = memberIdIndex,
                          boardReplyContent = articleParameter.content,
                          boardReplierIp = articleParameter.updateIp,
                          boardRepliedDate = articleParameter.updateDate)
    

'''
Insert LikesOnRepliesBoard
'''
def insert_likes_on_reply_of_board(boardReplyIndex, memberIdIndex): 
    return LikesOnReplyOfBoard(boardReplyIndex = boardReplyIndex,
                               boardReplyLikerIdIndex = memberIdIndex)
    
    
'''
Board Article Like Counting
'''
def update_article_like_counting(articleIndex, LIKE_INCREASE = 1):
    dao.query(ArticlesOnBoard).\
        filter(ArticlesOnBoard.articleIndex == articleIndex).\
        update(dict(sumOfLikeCount = ArticlesOnBoard.sumOfLikeCount + LIKE_INCREASE))   
        
        
'''
Board Article isLike update
'''
def update_article_is_like(articleIndex, memberIdIndex, isLikeCancelled = ENUMResources().const.FALSE):
    dao.query(LikesOnBoard).\
        filter(and_(LikesOnBoard.articleIndex == articleIndex,
                    LikesOnBoard.boardLikerIdIndex == memberIdIndex)).\
        update(dict(isLikeCancelled = isLikeCancelled))
             
'''
Board Article Modify
'''
def update_article_modify(articleIndex, problemIndex, articleType, articleParameter, isDeleted = ENUMResources().const.FALSE):
    dao.query(ArticlesOnBoard).\
        filter(ArticlesOnBoard.articleIndex == articleIndex,
               ArticlesOnBoard.isDeleted == isDeleted).\
               update(dict(problemIndex = problemIndex, 
                           articleType = articleType,
                           title = articleParameter.title,
                           content = articleParameter.content,
                           updateIp = articleParameter.updateIp,
                           updateDate = articleParameter.updateDate))
               
               
'''
Board Article delete
'''
def update_article_delete(articleIndex, isDeleted = ENUMResources().const.TRUE): 
    dao.query(ArticlesOnBoard).\
        filter(ArticlesOnBoard.articleIndex == articleIndex).\
        update(dict(isDeleted = isDeleted))  
        
                    
'''
Replies on Board
'''
def select_replies_on_board(articleIndex, boardReplyIndex = None, isDeleted = ENUMResources().const.FALSE):
    return dao.query(RepliesOnBoard).\
               filter(and_((RepliesOnBoard.articleIndex == articleIndex if articleIndex
                            else RepliesOnBoard.boardReplyIndex == boardReplyIndex),
                           RepliesOnBoard.isDeleted == isDeleted))
               

'''
Replies on Board isLike
'''
def select_replies_on_board_is_like(boardReplyIndex, memberIdIndex):
    return dao.query(LikesOnReplyOfBoard).\
               filter(and_(LikesOnReplyOfBoard.boardReplyIndex == boardReplyIndex,
                           LikesOnReplyOfBoard.boardReplyLikerIdIndex == memberIdIndex))
               

'''
Replies on Board isLike
'''
def select_replies_on_board_like(repliesOnBoard, memberIdIndex):
    return dao.query(LikesOnReplyOfBoard).\
               join(repliesOnBoard,
                    and_(LikesOnReplyOfBoard.boardReplyIndex == repliesOnBoard.c.boardReplyIndex,
                         LikesOnReplyOfBoard.boardReplyLikerIdIndex == memberIdIndex))
               

'''
Repllies on Board Like Counting
'''
def update_replies_on_board_like_counting(boardReplyIndex, LIKE_INCREASE = 1):
    dao.query(RepliesOnBoard).\
        filter(RepliesOnBoard.boardReplyIndex == boardReplyIndex).\
        update(dict(sumOfLikeCount = RepliesOnBoard.sumOfLikeCount + LIKE_INCREASE))  
        
'''
Replies on Board is LIke
'''
def update_replies_on_board_is_like(boardReplyIndex, memberIdIndex, isLikeCancelled = ENUMResources().const.FALSE):
    dao.query(LikesOnReplyOfBoard).\
        filter(and_(LikesOnReplyOfBoard.boardReplyIndex == boardReplyIndex,
                    LikesOnReplyOfBoard.boardReplyLikerIdIndex == memberIdIndex)).\
        update(dict(isLikeCancelled = isLikeCancelled))


'''
Replies on Board Update
'''
def update_replies_on_board_modify(boardReplyIndex, replyParameter):
    dao.query(RepliesOnBoard).\
        filter(RepliesOnBoard.boardReplyIndex == boardReplyIndex).\
        update(dict(boardReplyContent = replyParameter.content,
                    boardReplierIp = replyParameter.updateIp,
                    boardRepliedDate = replyParameter.updateDate))
        
        
'''
Repllies on Board delete
'''
def update_replies_on_board_delete(boardReplyIndex, isDeleted = ENUMResources().const.TRUE):
    dao.query(RepliesOnBoard).\
        filter(RepliesOnBoard.boardReplyIndex == boardReplyIndex).\
        update(dict(isDeleted = isDeleted)) 



'''
 DB Select Notices
 권한 별로 공지 가져오기
'''
def select_notices(memberIdIndex, isLogin):
    # Notices Layer
    
        # 공지만
    # islogin
    if isLogin:
        articlesOnBoard = select_articles().subquery()
    # Not login
    else:
        articlesOnBoard = select_server_notices().subquery()
                                  
    # List sort
    try:
                # 과목 공지글
        # Get ServerAdministrator is All, CourseAdministrators, Users is server and course Notice
                # 서버 관리자는 모든 공지
                # 과목 관리자 및 유저는 담당 과목 공지
        articleNoticeRecords = select_sorted_articles(articlesOnBoard)
    except Exception:
        articleNoticeRecords = []
       
    return articleNoticeRecords


''' 
Ger ServerNotices
'''
def select_server_notices(articleType = ENUMResources().const.NOTICE, isDeleted = ENUMResources().const.FALSE):
    return dao.query(ArticlesOnBoard).\
               filter(and_(ArticlesOnBoard.articleType == articleType,
                           ArticlesOnBoard.isDeleted == isDeleted)) 