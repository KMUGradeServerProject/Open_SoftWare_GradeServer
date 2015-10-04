# -*- coding: utf-8 -*-
'''
    GradeSever.controller.board
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    로그인 확인 데코레이터와 로그인 처리 모듈.

   :copyright:(c) 2015 by KookminUniv

'''

import socket

from flask import render_template, request, session, redirect, url_for, Response
from datetime import datetime
from sqlalchemy import exc

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilMessages import unknown_error
from GradeServer.utils.utilArticleQuery import select_articles, select_article, select_sorted_articles, select_article_is_like,\
                                               select_replies_on_board, select_replies_on_board_is_like, select_replies_on_board_like, update_view_reply_counting,\
                                               update_article_like_counting, update_article_is_like, update_replies_on_board_like_counting,\
                                               update_replies_on_board_is_like, update_replies_on_board_delete, update_replies_on_board_modify, update_article_delete,\
                                               insert_articles_on_board, insert_likes_on_board, insert_replies_on_board, insert_likes_on_reply_of_board, update_article_modify
from GradeServer.utils.utilUserQuery import join_member_id
from GradeServer.utils.utilProblemQuery import join_problems_name
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utils import get_request_value, is_authority

from GradeServer.utils.parameter.filterFindParameter import FilterFindParameter
from GradeServer.utils.parameter.articleParameter import ArticleParameter

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.languageResources import LanguageResources
from GradeServer.resource.sessionResources import SessionResources

from GradeServer.database import dao
from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer 

@GradeServer.teardown_request
def close_db_session(exception = None):
    '''요청이 완료된 후에 db연결에 사용된 세션을 종료함'''
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))


'''
게시판을 과목별 혹은 전체 통합으로
보여주는 페이지

filterCondition and keyWord is Search Event
'''
@GradeServer.route('/article_board?filterCondition=<filterCondition>&keyWord=<keyWord>&page=<int:pageNum>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def article_board(filterCondition, keyWord, pageNum):    
    try:
        # get Articles
        articlesOnBoard = select_articles().subquery()
        # Get MemberId
        articlesOnBoard = join_member_id(articlesOnBoard,
                                         subMemberIdIndex = articlesOnBoard.c.\
                                                                            writerIdIndex).subquery()
                                                                    
        # Get Problem Name
        articlesOnBoard = join_problems_name(articlesOnBoard,
                                             subProblemIndex = articlesOnBoard.c.problemIndex).subquery()
                # 과목 공지글
        try:  
            articleNoticeRecords = select_sorted_articles(articlesOnBoard).all()
        except Exception:
            articleNoticeRecords = []
            
                # 과목 게시글
        try:
            # Search Event
            if request.method == 'POST':
                for form in request.form:
                    # FilterCondition
                    if 'keyWord' != form:
                        filterCondition = form
                        keyWord = get_request_value(form = request.form,
                                                    name = 'keyWord')
                        pageNum = 1
                    
                if not keyWord:
                    keyWord = ' '
            articlesOnBoardSub = select_sorted_articles(articlesOnBoard,
                                                        FilterFindParameter(filterCondition,
                                                                            (keyWord if keyWord != ' '
                                                                             else '')),
                                                        articleType = ENUMResources().const.QUESTION)
            count = select_count(articlesOnBoardSub.subquery().\
                                                    c.articleIndex).first().\
                                                                    count
            articleRecords = get_page_record(articlesOnBoardSub,
                                             pageNum = pageNum,
                                             LIST = int(20)).all()
        except Exception:
            count = 0
            articleRecords = []
            
        return render_template(HTMLResources().const.BOARD_HTML,
                               articleRecords = articleRecords,
                               articleNoticeRecords = articleNoticeRecords,
                               pages = get_page_pointed(pageNum,
                                                        count,
                                                        int(20)),
                                                              # 검색시 FilterCondition List
                               Filters = [LanguageResources().const.All,
                                          LanguageResources().const.Writer,
                                          LanguageResources().const.Title],
                               filterCondition = filterCondition,
                               keyWord = keyWord)  
    except Exception as e:
        return unknown_error(e)


'''
게시판 공지만 과목별 혹은 전체 통합으로
보여주는 페이지
filterCondition and keyWord is Search Event
'''
@GradeServer.route('/article_notice?filterCondition=<filterCondition>&keyWord=<keyWord>&page=<int:pageNum>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def article_notice(filterCondition, keyWord, pageNum): 
    try:
        # get Notice Articles
        articlesOnBoard = select_articles().subquery()

        # Get MemberId
        articlesOnBoard = join_member_id(articlesOnBoard,
                                         subMemberIdIndex = articlesOnBoard.c.\
                                                                            writerIdIndex).subquery()
                                                            
        # Get Problem Name
        articlesOnBoard = join_problems_name(subquery = articlesOnBoard,
                                             subProblemIndex = articlesOnBoard.c.problemIndex).subquery()
                # 과목 공지글 
        try:
            if request.method == 'POST':
                for form in request.form:
                    # FilterCondition
                    if 'keyWord' != form:
                        filterCondition = form
                        keyWord = get_request_value(form = request.form,
                                                    name = 'keyWord')
                        pageNum = 1

                if not keyWord:
                    keyWord = ' '                
            # Notices Sorted
            articleNoticeRecords = select_sorted_articles(articlesOnBoard,
                                                          FilterFindParameter(filterCondition,
                                                                              (keyWord if keyWord != ' '
                                                                               else '')),
                                                          isAll = True)        
            # Get Notices count
            count = select_count(articleNoticeRecords.subquery().\
                                                      c.\
                                                      articleIndex).first().\
                                                                    count
            # Get Notices in Page                                                                           
            articleNoticeRecords = get_page_record(articleNoticeRecords,
                                                   pageNum = pageNum).all()
        except Exception:
            count = 0
            articleNoticeRecords = []
        
        return render_template(HTMLResources().const.ARTICLE_NOTICE_HTML,
                               articleNoticeRecords = articleNoticeRecords,
                               pages = get_page_pointed(pageNum,
                                                        count),
                                                              # 검색시 FilterCondition List
                               Filters = [LanguageResources().const.All,
                                          LanguageResources().const.Writer,
                                          LanguageResources().const.Title],
                               filterCondition = filterCondition,
                               keyWord = keyWord)
    except Exception as e:
        return unknown_error(e)
                            

'''
Article Click Like
'''
@GradeServer.route('/article_like_click?articleIndex=<int:articleIndex>', methods = ['POST'])
@login_required
@check_invalid_access
def article_like_click(articleIndex):
        # 게시글 좋아요  Push
        # 내가 게시글에 누른 좋아요 정보
    try:
        isLikeCancelled = select_article_is_like(articleIndex,
                                                 memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                                                                                    isLikeCancelled
    except Exception:
        # Non-Exist Case
        isLikeCancelled = None
            
        # 좋아요를 누른적 없을 때
    if not isLikeCancelled:
        # Insert Like
        dao.add(insert_likes_on_board(articleIndex,
                                      memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]))
        # Counting +1
        LIKE_INCREASE = 1
    else:
                                # 다시 좋아요 누를 때
        if isLikeCancelled == ENUMResources().const.TRUE:
            # Counting +1
            LIKE_INCREASE = 1
            isLikeCancelled = ENUMResources().const.FALSE
                                # 좋아요 취소 할 때
        else:  # if it's already exist then change the value of 'pushedLike'
            # Counting -1
            LIKE_INCREASE = -1
            isLikeCancelled = ENUMResources().const.TRUE
            
        # Update Like
        update_article_is_like(articleIndex,
                               memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                               isLikeCancelled = isLikeCancelled)
    # Article 좋아요 갯수 올리기
    update_article_like_counting(articleIndex,
                                 LIKE_INCREASE = LIKE_INCREASE)
    
    
    try:
        dao.commit()
        # return like count
        try:
            count =  select_article(articleIndex = articleIndex).first().\
                                                                 sumOfLikeCount
        except Exception:
            count = 0
        
        return Response(str(count))
    except Exception:
        dao.rollback()
        
    return Response()


'''
Article Reply Click Like
'''
@GradeServer.route('/board_reply_like_click?boardReplyIndex=<int:boardReplyIndex>', methods = ['POST'])
@login_required
@check_invalid_access
def board_reply_like_click(boardReplyIndex):
        # 댓글 좋아요
        # 내가 Reply에 누른 좋아요 정보
    try:
        isReplyLike = select_replies_on_board_is_like(boardReplyIndex,
                                                      memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                                                                                         isLikeCancelled
    except Exception:
        # Non-Exist Case
        isReplyLike = None
        
                        # 좋아요를 누른적 없을 때
    if not isReplyLike:
        # Insert Like
        dao.add(insert_likes_on_reply_of_board(boardReplyIndex,
                                               memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]))
        # Counting +1
        LIKE_INCREASE = 1
    else:
                                # 다시 좋아요 누를 때
        if isReplyLike == ENUMResources().const.TRUE:
            # Counting +1
            LIKE_INCREASE = 1
            isLikeCancelled = ENUMResources().const.FALSE
                                # 좋아요 취소 할 때
        else:  # if it's already exist then change the value of 'pushedLike'
            # Counting -1
            LIKE_INCREASE = -1
            isLikeCancelled = ENUMResources().const.TRUE
            
        # Update Like
        update_replies_on_board_is_like(boardReplyIndex,
                                        memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                        isLikeCancelled = isLikeCancelled)
            
    # Like or UnLIke
    update_replies_on_board_like_counting(boardReplyIndex,
                                          LIKE_INCREASE = LIKE_INCREASE)
    try:
        dao.commit()
        
        # return like count
        try:
            count = select_replies_on_board(articleIndex = None,
                                            boardReplyIndex = boardReplyIndex).first().\
                                                                               sumOfLikeCount
        except Exception:
            count = 0
        
        return Response(str(count))
    except Exception:
        dao.rollback()
        
    return Response()
    
    
'''
게시글을 눌렀을 때 
글 내용을 보여주는 페이지
'''
@GradeServer.route('/read?articleIndex=<int:articleIndex>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def read(articleIndex, error = None):
    ''' when you push a title of board content '''
    try:
                # 내가 게시글에 누른 좋아요 정보
        try:
            isLikeCancelled = select_article_is_like(articleIndex,
                                                     memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                                                                                        isLikeCancelled
        except Exception:
            # Non-Exist Case
            isLikeCancelled = None
            
        if request.method == 'POST':
            authorityCheck = is_authority(session[SessionResources().const.AUTHORITY])
            for form in request.form:
                
                                # 댓글 달기
                if form == 'writeArticleReply':
                                        # 새로운 댓글 정보articleParameter
                    boardReplyContent = get_request_value(form = request.form,
                                                          name = 'writeArticleReply')
                    
                    if boardReplyContent:
                        dao.add(insert_replies_on_board(articleIndex,
                                                        session[SessionResources().const.MEMBER_ID_INDEX],
                                                        ArticleParameter(title = None,
                                                                         content = boardReplyContent,
                                                                         updateIp = socket.gethostbyname(socket.gethostname()),
                                                                         updateDate = datetime.now())))
                        # remove duplicated read count
                        update_view_reply_counting(articleIndex,
                                                   VIEW_INCREASE = -1,
                                                   REPLY_INCREASE = 1)
                        
                    break 
                                # 댓글 삭제   
                elif 'deleteArticleReply' in form:
                    # Get Reply Index
                    replyIndex = len('deleteArticleReply')
                    boardReplyIndex = int(form[replyIndex:])
                                          
                    try:
                        writerIndex = select_replies_on_board(articleIndex = None,
                                                              boardReplyIndex = boardReplyIndex).first()
                    except Exception:
                        writerIndex = None
                    if authorityCheck[0]\
                       or writerIndex.boardReplierIdIndex == session[SessionResources().const.MEMBER_ID_INDEX]:
                            
                        update_replies_on_board_delete(boardReplyIndex,
                                                       isDeleted = ENUMResources().const.TRUE)
                        # remove duplicated read count
                        update_view_reply_counting(articleIndex,
                                                   VIEW_INCREASE = -1,
                                                   REPLY_INCREASE = -1)
                    else:
                        error = LanguageResources().const.GetOutHere
                    
                    break 
                # Commit Modify
                elif 'modifyArticleReplyContent' in form:
                    replyIndex = len('modifyArticleReplyContent')
                    boardReplyIndex = int(form[replyIndex:])
                    try:
                        writerIndex = select_replies_on_board(articleIndex = None,
                                                              boardReplyIndex = boardReplyIndex).first()
                    except Exception:
                        writerIndex = None
                    if writerIndex.boardReplierIdIndex == session[SessionResources().const.MEMBER_ID_INDEX]:
                        boardReplyContent = get_request_value(form = request.form,
                                                              name = 'modifyArticleReplyContent{0}'.format(form[replyIndex:]))
                        
                        if boardReplyContent:
                            #update comment
                            update_replies_on_board_modify(boardReplyIndex,
                                                           ArticleParameter(title = None,
                                                                            content = boardReplyContent,
                                                                            updateIp = socket.gethostbyname(socket.gethostname()),
                                                                            updateDate = datetime.now()))
                            # remove duplicated read count
                            update_view_reply_counting(articleIndex,
                                                       VIEW_INCREASE = -1)
                    else:
                        error = LanguageResources().const.GetOutHere
                        
                    break
                
                            # 게시물 삭제
                elif form == 'deleteArticle':
                    try:
                        writerIndex = select_article(articleIndex = articleIndex).first()
                    except Exception:
                        writerIndex = None
                    if authorityCheck[0]\
                       or writerIndex.writerIdIndex == session[SessionResources().const.MEMBER_ID_INDEX]:
                        update_article_delete(articleIndex,
                                              isDeleted = ENUMResources().const.TRUE)                    
                        # Commit Exception
                        try:
                            dao.commit()
                        except Exception:
                            dao.rollback()
                            error = LanguageResources().const.DBFailed
                            
                        return redirect(url_for(RouteResources().const.ARTICLE_BOARD,
                                                filterCondition = ' ',
                                                keyWord = ' ',
                                                pageNum = 1))
                    else:
                        error = LanguageResources().const.GetOutHere
            # end Loop
            # Commit Exception
            try:
                dao.commit()
            except Exception:
                dao.rollback()
                error = LanguageResources().const.DBFailed
            
        # Get or Post
                # 게시글 정보
        try:
            articlesOnBoard = select_article(articleIndex).subquery()
                
            #Get ProblemName
            articlesOnBoard = join_problems_name(subquery = articlesOnBoard,
                                                 subProblemIndex = articlesOnBoard.c.problemIndex).subquery()
            # Get MemberId
            articlesOnBoard = join_member_id(articlesOnBoard,
                                             subMemberIdIndex = articlesOnBoard.c.\
                                                                                 writerIdIndex).first()
        except Exception:
            articlesOnBoard = []
            
        try:
            # replies 정보
            repliesOnBoardRecords = select_replies_on_board(articleIndex).subquery()
            # Get MemberId
            repliesOnBoardRecords = join_member_id(repliesOnBoardRecords,
                                                   subMemberIdIndex = repliesOnBoardRecords.c.\
                                                                                            boardReplierIdIndex)
                        # 내가 게시글 리플에 누른 좋아요 정보
            repliesOnBoardIsLikeRecords = select_replies_on_board_like(repliesOnBoardRecords.subquery(),
                                                                       memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).all()
            repliesOnBoardRecords = repliesOnBoardRecords.all()  
        except Exception:
            repliesOnBoardIsLikeRecords = []
            repliesOnBoardRecords = []
            
                # 읽은 횟수 카운팅
        update_view_reply_counting(articleIndex,
                                   VIEW_INCREASE = 1)
        
        # Commit Exception
        try:
            dao.commit()
        except Exception:
            dao.rollback()
            
        return render_template(HTMLResources().const.ARTICLE_READ_HTML,
                               articlesOnBoard = articlesOnBoard,
                               repliesOnBoardRecords = repliesOnBoardRecords,
                               repliesOnBoardIsLikeRecords = repliesOnBoardIsLikeRecords,
                               isLikeCancelled = isLikeCancelled,
                               error = error)
    except Exception:
        # Exception View    
        return redirect(url_for(RouteResources().const.ARTICLE_BOARD,
                                pageNum = 1))


'''
게시판에 글을 쓰는 페이지
'''
@GradeServer.route('/write?articleIndex=<int:articleIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def write(articleIndex, error = None):
    articleType, problemIndex, title, content, articlesOnBoard = None, None, None, None, None
    try:
        # Modify Case
        if articleIndex: 
            try:
                articlesOnBoard = select_article(articleIndex).subquery()
                articlesOnBoard = join_problems_name(subquery = articlesOnBoard,
                                                     subProblemIndex = articlesOnBoard.c.problemIndex).first()
            except Exception:
                articlesOnBoard = []
                        
                # 작성시 빈칸 검사
        if request.method == 'POST':
            if not articleIndex\
               or articlesOnBoard.writerIdIndex == session[SessionResources().const.MEMBER_ID_INDEX]:
                # Get ProblemIndex
                problemIndex = get_request_value(form = request.form,
                                                 name = 'problemIndex')
                # Get ArticleType
                articleType = get_request_value(form = request.form,
                                                name = 'articleType')
                                # 타이틀 가져오기
                title = get_request_value(form = request.form,
                                          name = 'title')
                # Get Exist Content
                content = get_request_value(form = request.form,
                                            name = 'content')
                
                # Success Post
                if title and len(title) <= 100\
                   and content:
                    updateDate = datetime.now()
                    updateIp = socket.gethostbyname(socket.gethostname())
                                    # 새로 작성
                    if not articleIndex:
                        newPost = insert_articles_on_board(problemIndex = problemIndex,
                                                           memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                                           articleType = articleType,
                                                           articleParameter = ArticleParameter(title = title,
                                                                                               content = content,
                                                                                               updateDate = updateDate,
                                                                                               updateIp = updateIp))
                        dao.add(newPost)
                        # Commit Exception
                        try:
                            dao.commit()
                        except exc.SQLAlchemyError:
                            dao.rollback()
                            error = LanguageResources().const.DBFailed
                            
                        return redirect(url_for(RouteResources().const.ARTICLE_BOARD,
                                                filterCondition = ' ',
                                                keyWord = ' ',
                                                pageNum = 1))
                                        # 게시물 수정    
                    else:
                                                # 수정 할 글 정보
                        update_article_modify(articleIndex,
                                              problemIndex = problemIndex,
                                              articleType = articleType,
                                              articleParameter = ArticleParameter(title = title,
                                                                                  content = content,
                                                                                  updateIp = updateIp,
                                                                                  updateDate = updateDate))
                        
                        # Commit Exception
                        try:
                            dao.commit()
                        except exc.SQLAlchemyError:
                            dao.rollback()
                            error = LanguageResources().const.DBFailed
                        
                        return redirect(url_for(RouteResources().const.ARTICLE_READ,
                                                articleIndex = articleIndex))
            else:
                error = LanguageResources().const.GetOutHere
                
        return render_template(HTMLResources().const.ARTICLE_WRITE_HTML,
                               articlesOnBoard = articlesOnBoard,
                               articleTypes = [ENUMResources().const.NOTICE,
                                               ENUMResources().const.QUESTION,
                                               ENUMResources().const.NORMAL],
                               articleType = articleType,
                               problemIndex = problemIndex,
                               title = title,
                               content = content,
                               error = error)
    except Exception as e:
        # Unknown Error
        return unknown_error(e)
