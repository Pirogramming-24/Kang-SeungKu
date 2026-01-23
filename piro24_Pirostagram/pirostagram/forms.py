from django import forms
from .models import Post
from .models import Comment, Story

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': '문구를 입력하세요...',
                'style': 'width: 100%; height: 100px; border: 1px solid #dbdbdb;'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': '댓글 달기...',
                'style': 'border:none; outline:none; width:100%;'
            })
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['photo']
        widgets = {
            # [수정] 위에서 만든 커스텀 위젯 사용
            'photo': MultipleFileInput(attrs={'multiple': True})
        }

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'style': 'width: 100%; height: 100px; border: 1px solid #dbdbdb;'
            }),
        }