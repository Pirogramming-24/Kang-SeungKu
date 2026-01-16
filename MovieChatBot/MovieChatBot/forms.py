from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'poster', 'release_year', 'genre', 'rating', 'director', 'actors', 'running_time', 'content']