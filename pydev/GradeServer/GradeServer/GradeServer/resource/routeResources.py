

class RouteResources(object):
    """ROUTE Resource Static Class"""
    
    from GradeServer.resource import const

    # Login routes
    const.SIGN_IN = '.sign_in'
    const.SIGN_IN_NEWPAGE = '.sign_in_newPage'
    
    # Board routes
    const.ARTICLE_BOARD = '.article_board'
    const.ARTICLE_READ = '.read'

    # Team routes
    const.TEAM = '.team'
    
    # User routes
    const.ID_CHECK = '.id_check'
    const.EDIT_PERSONAL = '.edit_personal'
    const.USER_HISTORY = '.user_history'
    
    # Problem routes
    const.PROBLEM_LIST = '.problem_list'
    const.PROBLEM_RECORD ='.problem_record'