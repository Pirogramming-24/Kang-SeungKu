from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['created_at', 'updated_at']
        fields = '__all__'
        widgets = {
            'calorie': forms.TextInput(attrs={'placeholder': '분석 중...'}),
            'carbo': forms.TextInput(attrs={'placeholder': '분석 중...'}),
            'protein': forms.TextInput(attrs={'placeholder': '분석 중...'}),
            'fat': forms.TextInput(attrs={'placeholder': '분석 중...'}),
        }