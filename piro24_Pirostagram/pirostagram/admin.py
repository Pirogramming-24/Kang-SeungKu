# pirostagram/admin.py

from django.contrib import admin
from .models import Post, Comment, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 관리자 목록 화면에서 보여줄 필드 설정
    list_display = ['id', 'author', 'short_content', 'created_at']
    # 클릭하면 상세 페이지로 들어갈 수 있는 필드
    list_display_links = ['id', 'short_content']
    
    # 내용이 길면 앞부분만 보여주는 함수
    def short_content(self, obj):
        return obj.content[:20] + "..." if len(obj.content) > 20 else obj.content
    short_content.short_description = "내용 요약"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'content', 'created_at']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'intro']