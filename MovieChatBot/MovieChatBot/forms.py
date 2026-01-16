from django import forms
from .models import Movie, Review

# 1. 영화 정보 입력 폼 (화면 상단 영역)
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        # 사용자가 직접 입력해야 하는 필드들만 지정
        fields = ['title', 'release_year', 'director', 'genre', 'actors', 'running_time', 'poster_image']
        
        # UI 스타일과 Placeholder 설정 (형님 사진에 있는 텍스트 그대로 적용)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '영화 제목을 입력하세요'
            }),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '개봉 년도 (예: 2024)'
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '감독 이름을 입력하세요'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'actors': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '주연배우를 입력하세요 (여러 명인 경우 ,로 구분)'
            }),
            'running_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '러닝타임 (분 단위)'
            }),
            'poster_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        
        labels = {
            'title': '영화 제목',
            'release_year': '개봉 년도',
            'director': '감독',
            'genre': '장르',
            'actors': '주연배우',
            'running_time': '러닝타임(분)',
            'poster_image': '포스터 이미지',
        }

# 2. 리뷰 정보 입력 폼 (화면 하단 영역)
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': '영화에 대한 리뷰를 작성해주세요',
                'rows': 5
            }),
        }
        
        labels = {
            'rating': '별점',
            'content': '리뷰 내용',
        }