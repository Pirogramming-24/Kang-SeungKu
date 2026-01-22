from django.urls import path
from . import views

app_name = 'pirostagram'

urlpatterns = [
    path('', views.main, name='main'),
]