from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'), 
    path('create/', views.movie_create, name='movie_create'), 
    path('<int:pk>/update/', views.movie_update, name='movie_update'), 
    path('<int:pk>/delete/', views.movie_delete, name='movie_delete'), 
]