from django.urls import path
from . import views

app_name = 'SWIDEA_SITE'

urlpatterns = [
    # 1. 메인 및 아이디어 관련
    path('', views.idea_list, name='idea_list'), # 메인(리스트)
    path('idea/create/', views.idea_create, name='idea_create'), # 아이디어 등록
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'), # 아이디어 디테일
    path('idea/<int:pk>/update/', views.idea_update, name='idea_update'), # 아이디어 수정
    path('idea/<int:pk>/delete/', views.idea_delete, name='idea_delete'), # 아이디어 삭제
    
    # 2. 개발툴 관련
    path('devtool/', views.devtool_list, name='devtool_list'),
    path('devtool/create/', views.devtool_create, name='devtool_create'),
    path('devtool/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtool/<int:pk>/update/', views.devtool_update, name='devtool_update'),
    path('devtool/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),

    # [챌린지] AJAX 관련 URL
    path('idea/<int:pk>/star/', views.idea_star_ajax, name='idea_star_ajax'), # 찜하기 토글
    path('idea/<int:pk>/interest/', views.idea_interest_ajax, name='idea_interest_ajax'), # 관심도 조절
]