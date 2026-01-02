from django.apps import AppConfig
from django.urls import path
from . import views

class SwideaSiteConfig(AppConfig):
    name = 'SWIDEA_SITE'

urlpatterns = [
    # 나중에 여기에 path('', views.main, name='main') 등을 추가할 예정
]