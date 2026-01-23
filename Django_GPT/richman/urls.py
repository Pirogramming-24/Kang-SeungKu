from django.urls import path
from . import views

app_name = 'richman'

urlpatterns = [
    path('', views.main, name='main'),
    path('sentiment/', views.sentiment_view, name='sentiment'), 
    path('analyze/', views.analyze_view, name='analyze'),
    path('spam/', views.spam_view, name='spam'),
    path('ner/', views.ner_view, name='ner'),
    path('report/', views.report_view, name='report'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
]