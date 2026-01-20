from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_year', 'director', 'genre', 'actors', 'running_time', 'poster_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '영화 제목'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '예: 2025'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '감독 이름'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'actors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '주연 배우 (쉼표로 구분)'}),
            'running_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '분 단위'}),
            'poster_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '솔직한 리뷰를 남겨주세요', 'rows': 5}),
        }