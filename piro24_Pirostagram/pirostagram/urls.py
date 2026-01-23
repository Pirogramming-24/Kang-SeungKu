from django.urls import path
from . import views

app_name = 'pirostagram'

urlpatterns = [
    path('', views.main, name='main'),
    path('post/create/', views.post_create, name='post_create'),
    path('like/', views.post_like, name='post_like'),
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'), 
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('search/', views.search, name='search'),
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('users/<int:user_id>/follow/', views.follow, name='follow'),
    path('story/create/', views.story_create, name='story_create'), 
    path('post/update/<int:post_id>/', views.post_update, name='post_update'), 
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'), 
]