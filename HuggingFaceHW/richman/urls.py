from django.urls import path
from . import views

app_name = 'richman'

urlpatterns = [
    # 1. 메인 화면
    path('', views.main, name='main'),

    # 2. [기능 1] 감성 분석
    path('sentiment/', views.sentiment_view, name='sentiment'), # 화면 접속용
    path('analyze/', views.analyze_view, name='analyze'),       # AI 분석 동작용

    # 3. 나머지 기능들 (이게 없어서 에러가 났던 겁니다!)
    path('spam/', views.spam_view, name='spam'),
    path('ner/', views.ner_view, name='ner'),
    path('report/', views.report_view, name='report'),
]