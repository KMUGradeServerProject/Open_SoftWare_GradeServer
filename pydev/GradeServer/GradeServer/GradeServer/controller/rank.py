# -*- coding: utf-8 -*-


from flask import render_template, request

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utilUserQuery import select_members,\
                                            select_match_member_sub,\
                                            join_member_id,\
                                            select_match_member_id
from GradeServer.utils.utilRankQuery import select_ranks,\
                                            ranks_sorted
from GradeServer.utils.utilSubmissionQuery import select_last_submissions
from GradeServer.utils.utils import get_request_value
from GradeServer.utils.utilMessages import unknown_error

from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.database import dao

from GradeServer.GradeServer_logger import Log
from GradeServer import page_not_found
from GradeServer.GradeServer_blueprint import GradeServer


@GradeServer.teardown_request
def close_db_session(exception = None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))
        
        
"""
로그인한 유저가 랭크 페이지를 눌렀을 때
페이지 별로 보여줌
activeTabIndex is courseIndex
"""    
@GradeServer.route('/rank?page=<int:pageNum>&sortCondition=<sortCondition>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def rank(sortCondition, pageNum, error =None):
    
    # Not Accept URL Check
    if sortCondition not in (LanguageResources().const.Rate[1],
                             LanguageResources().const.SolvedProblems[1]):
        return page_not_found()
    
    try:
        #Searched MemberId
        memberId = None
        try:
            # Auto Complete MemberIds
            memberRecords = select_members().all()
        except Exception:
            memberRecords = []
            
        # Last Submission Max Count
        submissions = select_ranks(select_last_submissions().subquery()).subquery()
        submissions = join_member_id(submissions,
                                     subMemberIdIndex = submissions.c.memberIdIndex).subquery() 
        # records count
        try:
            count = select_count(submissions.c.memberIdIndex).first().\
                                                              count
        except Exception:
            count = 0

        # Paging Pointed
        pages = get_page_pointed(pageNum = pageNum,
                                 count = count)
        submissions = ranks_sorted(submissions,
                                   sortCondition = sortCondition)
        # Find MemberId 뷰 호출
        if request.method == 'POST':
            # Finding MemberId
            memberId = get_request_value(form = request.form,
                                             name = 'memberId')
            try:
                memberIdIndex = select_match_member_id(memberId).first().memberIdIndex
                            # 순차 탐색으로 찾아야 함
                for i in range(1, pages['allPage'] + 1):
                    # memberId in Pages 
                    ranks = get_page_record(submissions,
                                            pageNum = i).subquery()
                    # finding MemberId in Pages
                    if select_match_member_sub(ranks,
                                               memberIdIndex = memberIdIndex).first() != None:
                        # Finding move to page
                        pageNum = i
                        # searchLine Check
                        # RePaging Pointed
                        pages = get_page_pointed(pageNum = pageNum,
                                                 count = count)
                    
                        break
            except Exception:
                error = LanguageResources().const.NotExist
                # 랭크 정보
        try:
            rankMemberRecords = get_page_record(submissions,
                                                pageNum = pageNum).all()
        except Exception:
            rankMemberRecords = []
        
        return render_template(HTMLResources().const.RANK_HTML,
                               sortCondition =  sortCondition,
                               memberRecords = memberRecords,
                               rankMemberRecords = rankMemberRecords,
                               pages = pages,
                               memberId = memberId,
                               error = error) # 페이지 정보
    except Exception as e:
        return unknown_error(e)     

