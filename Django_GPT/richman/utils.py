from django.shortcuts import render

def login_required_alert(request):
    """
    비로그인 유저가 접근하면 
    1. '로그인 후 이용해주세요' 알림을 띄우고
    2. 로그인 페이지로 이동시키는 HTML을 반환함
    """
    # 로그인 후 원래 가려던 페이지로 돌아오게 하기 위해 'next' 파라미터 추가
    next_url = request.path 
    
    context = {
        'msg': '로그인 후 이용해주세요',
        'next_url': next_url
    }
    # 알림창을 띄워줄 임시 페이지 렌더링
    return render(request, 'alert_login.html', context)