# -*- coding: utf-8 -*-

class LanguageResources(object):
    from GradeServer.resource import const
    
    '''
    ==@@ Error Message
    '''
    const.LowerBrowser = ['현재 접속하신 브라우저에서는 기능이 제대로 작동하지 않습니다.\n다른 브라우저를 사용하시거나 익스플로러를 업데이트 해주시기 바랍니다.',
                          'Your Browser is Trash. Then must update or change browser']
    const.IE =['익스플로러 업데이트', 'InternetExploer Update']
    const.Chrome = ['구글 크롬 다운로드', 'Google Chrome Download']
    const.BrowserAddress = ['http://windows.microsoft.com/ko-kr/internet-explorer/download-ie',
                            'https://www.google.com/chrome/browser/desktop/index.html']
    const.MinTime = ['앞 시간 보다 작아야 합니다.', 'Minimum front Time']
    const.MinDate = ['앞 날짜보다 작아야 합니다.', 'Minimum front Date']
    const.LeastOneCheck = ['한 개 이상 체크해야 햡니다.', 'At least one check']
    const.FormatCheck = ['입력 포맷에 맞게 입력해주세요.', 'Please, Input Format Check']
    const.UnknownError = ['죄송 합니다. 알수 없는 에러 입니다', 'Sorry, Unknown Erros']
    const.WrongPassword = ['암호가 일치하지 않습니다.', 'The passwords do not match.']
    const.DBFailed = ['서버에 문제가 있습니다. 잠시 후에 시도해 주세요.', 'Sorry, Try late again']
    const.FormValidation = ['입력 데이터에 문제가 있는 데이터는 무시 되었습니다', 'Please, Form Validation']
    const.Exist = ['이미 존재하는 데이터 입니다.', 'Exist Data']
    const.NotExist = ['해당 데이터가 없습니다.', 'Not Exist Data']
    const.GetOutHere = ['꺼져', 'Get Out Here']
    const.FormTypeError = ['옳지 않은 형식 입니다.', 'Fail Form Type']
    const.FileType = ['csv 또는 txt 타입의 파일을 선택해 주세요.', 'Accept this type csv or txt']
    const.RejectRegisterUser = ['더이상 사용자를 등록 할 수 없습니다. ', 'Don\' register users']
    '''
    @@ Main Page
    '''
    const.TopCoder = ['이 주의 탑 코더', 'Top Coder of this week']
    const.Help = ['도움말', 'Help']
    const.Introduce = ['소개', 'introduce']
    const.Management = ['관리', 'management']
    
    '''
    @@ Navigation bar
    '''
    const.Problems = ['문제', 'Problems']
    const.Rank = ['순위', 'Rank']
    const.Board = ['게시판', 'Board']
    const.SignIn = ['로그인', 'Sign in']
    const.Team = ['팀', 'Team']
    const.SignUp = ['회원가입', 'Sign up']


    '''
    ==@@ Modal 
    '''
    const.All = ['전체', 'All']
    const.Check = ['선택', 'Check']
    const.Chance = ['힌트', 'Chance']
    const.ReallyDeletion = ['정말 삭제 하시겠습니까?', 'Do you really want to delete it?']
    const.NoSelect = ['선택을 해주세요', 'No items choosed']
    
    const.none = ['없음', 'None']
    
    '''
    ==@@ Manual page
    '''    
    const.Information = ['기본정보', 'Information']
    const.Precautions = ['주의사항', 'Precautions']
    const.Video = ['동영상', 'Video']
    
    '''
    ==@@ Member ID tab
    '''
    # common
    const.Account = ['개인 정보', 'Account']
    const.Notice = ['공지 사항', 'Notice']
    const.SignOut = ['로그 아웃', 'Sign out']
    
    # for administrator
    const.User = ['사용자', 'User']
    const.Service = ['기능', 'Service']
    
    # for user
    const.UserRecord = ['제출 정보', 'Record']
    
    
    '''
    @@ Problems page
    '''
    const.ProblemTitle = ['문제이름', 'Title']
    const.Difficulty = ['난이도', 'Difficulty']
    const.Score = ['점수', 'Score']
    const.Status = ['채점상태', 'Status']
    const.Count = ['제출횟수', 'Submitted Count']
    const.ProblemRecord = ['제출 현황', 'Problem Record']
    const.NeverSubmitted =['미 제출', 'Never Submitted']
    const.Judging = ['채점 중', 'Judging']
    const.Solved = ['정답', 'Solved']
    const.TimeOver = ['시간 초과', 'Time Over']
    const.MemoryOverflow = ['메모리 사용 초과', 'Memory Overflow']
    const.WrongAnswer = ['오답', 'Wrong Answer']
    const.CompileError = ['컴파일 오류', 'Compile Error']
    const.RuntimeError = ['런타임 오류', 'Runtime Error']
    const.ServerError = ['서버 오류', 'Server Error']
    const.TriedPeople = ['제출 한 사람', 'Tried People']
    const.SolvedPeople = ['맞힌 사람', 'Solved People']
    
    '''
    ==@@ Each problem
    '''
    const.UploadFiles = ['파일로 제출', 'Upload Files']
    const.WriteCode = ['코드 작성', 'Write Code']
    const.ProblemScript = ['문제 보기', 'Problem Script']
    const.Submission = ['제출', 'Submission']
    const.DataInputType = ['입력 방식', 'DataInputType']
    const.Language = ['사용 언어', 'Language']
    const.Theme = ['에디터 테마', 'Theme']
    const.Limitation = ['제한', 'Limitation']
    const.Time = ['시간', 'Time']
    const.Memory = ['메모리', 'Memory']
    const.Select = ['선택', 'Select']
    const.Runtime = ['실행시간', 'Runtime']
    const.FileSize = ['길이', 'Size']
    const.SubmissionDate = ['제출일', 'Submitted Date']
    const.NumberOfFiles = ['파일 개수 선택', 'Select The Number Of Files']
    const.SubmissionSuccess = ['제출 성공!', 'Submission Success!']
    
    
    '''
    ==@@ User's code
    '''
    const.DownloadCode = ['소스코드 다운로드', 'Download sourcecode']
    
    
    '''
    @@ Rank page
    '''
    const.Ranking = ['순위', 'Ranking']
    const.Comment = ['한마디', 'Comment']
    const.Tries = ['채점 횟수', 'Tries']
    const.SolvedProblems = ['맞힌 문제 수', 'Solved Problems']
    const.Rate = ['정답률', 'Rate']
    const.Find = ['찾기', 'Find']
    
    
    '''
    @@ Board page
    '''
    const.Number = ['번호', 'Number']
    const.ArticleType = ['분류', 'Type']
    const.Question = ['질문', 'Question']
    const.Normal =['잡담', 'Normal']
    const.Title = ['제목', 'Title']
    const.Content = ['내용', 'Content']
    const.Writer = ['작성자', 'ID']
    const.UpdateDate = ['작성일', 'Date']
    const.ViewCount = ['조회수', 'View']
    const.Like = ['좋아요', 'Like']
    const.Write = ['글쓰기', 'Write']
    
    
    ''' 
    ==@@ article
    '''
    const.Edit = ['수정', 'Edit']
    
    
    '''
    @@ ID Check
    '''
    const.IdentificationCheck = ['암호 확인', 'Identification Check']
    const.Confirm = ['확인', 'Confirm']
    
    
    '''
    @@ Account
    '''
    const.DetailInformation = ['세부 정보', 'Detail Information']
    const.PersonalInformation = ['개인 정보', 'Personal Information']
    const.ID = ['아이디', 'ID']
    const.Password = ['암호', 'Password']
    const.Name = ['이름', 'Name']
    const.ContactNumber = ['연락처', 'Contact Number']
    const.Email = ['이메일', 'E-mail']
    
    const.Code = ['코드', 'Code']
    const.Administrator = ['관리자', 'Administrator']
    const.Done = ['확인', 'Done']
    
    
    '''
    @@ Problem management
    '''
    const.Problem = ['문제', 'Problem']
    const.AllInputCaseInOneFile =['파일 하나로 채점', 'All Input Case In One File']
    const.Solution = ['정적 채점', 'Solution']
    const.Checker = ['동적 채점', 'Checker']
    const.CheckType = ['채점 타입', 'CheckType']
    const.GoldLevel = ['골드', 'Gold']
    const.SilverLevel = ['실버', 'Silver']
    const.BronzeLevel = ['브론즈', 'Bronze']
    const.ProblemId = ['문제번호', 'Problem ID']
    const.Addition = ['추가', 'Addition']
    const.ProblemUpload = ['업로드', 'Upload']
    const.Close = ['닫기', 'Close']
    const.Modification = ['수정', 'Modification']
    const.Deletion = ['삭제', 'Deletion']
    const.HintView = ['힌트 보기 ', 'use hint']
    const.HintCount = ['회 가능',  'Available']
    const.EmptyHint = ['힌트 횟수를 모두 소모하였거나 힌트 대상 과목이 아니므로 힌트 사용이 불가합니다.', 'hint count is empty or This course has been banned hint']
     
    '''
    @@ User management
    '''
    const.Authority = ['권한', 'Authority']
    const.LastAccess = ['최근 접속일', 'Last Access']
    const.RegisteredUser = ['등록 인원', 'Registerd Users']
    
    
    '''
    ==@@ User addition
    '''
    const.AddLine = ['줄 추가', 'Add line']
    
    
    '''
    @@ Submission management
    '''
    const.Detail = ['자세히', 'Detail']
    const.DetailMode = ['자세히 보기', 'Detail mode']
    const.Summary = ['요약', 'Summary']
    const.SummaryMode = ['간략히 보기', 'Summary mode']
    const.History = ['기록', 'History']


    '''
    @@ Board
    '''
    const.NewArticle = ['새 글', 'New Article']
    const.Post = ['게시글', 'Post']
    const.DisLike = ['취소', 'DisLike']
    const.Reply = ['댓글', 'Comment']

    '''
    @@ Master py
    '''
    const.SolutionCheckerDirError = ['솔루션이나 체커 폴더가 없습니다', 'There is no \'SOLUTION\' or \'CHECKER\' directory']
    const.RemoveSpaceError = ['파일 이름에서 공백을 제거하는 도중 에러가 발생했습니다','Error has been occurred while removing space on file names']
    const.GetCurrentDirError = ['현재 경로를 얻는 도중 에러가 발생했습니다','Error has been occurred while getting current path']
    const.ChangeDirError = ['경로를 변경하는 도중 에러가 발생했습니다','Error has been occurred while changing directory']
    const.RenameFileError = ['파일 이름을 변경하는도중 에러가 발생했습니다','Error has been occurred while renaming file']
    const.MoveShellError = ['.sh 파일을 문제 in/out 파일 경로로 이동할 수 없습니다','Can not move .sh to problem in/out file path']
    const.RemoveShellError = ['.sh 파일을 지울 수 없습니다', 'Can not remove .sh file']
    const.UploadingFileError = ['파일 업로딩 에러', 'Uploading file error']
    const.ListingFilesError = ['파일이름을 읽는 도중에 에러가 발생했습니다', 'Error has been occurred while listing file names']
    const.ClosingFileError = ['문제 정보 파일을 닫는 도중 에러가 발생했습니다', 'Error has been occurred while closing problem meta file']
    const.ReadingFileError = ['문제 정보 파일을 읽는 도중 에러가 발생했습니다', 'Error has been occurred while reading problem meta file(.txt)']
    const.NotExistPDF = ['문제 pdf 파일이 존재하지 않습니다', 'problem pdf doesn\'s exist']
    const.DeleteFolderError = ['tmp 폴더를 삭제할 수 없습니다','Cannot delete \'tmp\' folder']
    const.DifficultyCharError = ['난이도는 숫자여야 합니다','Difficulty must be a number']
