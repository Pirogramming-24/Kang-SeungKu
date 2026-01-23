# pirostagram/models.py

from django.db import models
from django.contrib.auth.models import User 

class Post(models.Model):
    # 작성자 (User 모델과 1:N 관계, 유저 삭제시 게시글도 삭제)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # 게시글 사진 (media/posts/연/월/일 폴더에 저장됨)
    photo = models.ImageField(upload_to='posts/%Y%m%d')
    
    # 게시글 내용 (빈칸 허용 X)
    content = models.TextField()
    
    # 좋아요 (User와 N:M 관계, 좋아요 누른 사람 목록)
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)
    
    # 작성 시간 (자동 저장)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 수정 시간 (자동 업데이트)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username}의 게시글 - {self.content[:10]}'


class Comment(models.Model):
    # 어떤 게시글에 달린 댓글인지 (Post와 1:N 관계)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # 댓글 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 댓글 내용
    content = models.CharField(max_length=200)
    
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 댓글 수정 시간
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} - {self.content}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='profile/default.png')
    intro = models.CharField(max_length=60, blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username}의 프로필'
    
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    photo = models.ImageField(upload_to='stories/%Y%m%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}의 스토리'