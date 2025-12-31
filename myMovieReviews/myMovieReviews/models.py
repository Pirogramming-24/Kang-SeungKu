from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Review(models.Model) :
    title = models.CharField(max_length=50)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    rating = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)] # 0.0 ~ 10.0 제한
    )

    director = models.CharField(max_length=100) 
    actors = models.CharField(max_length=200)   
    running_time = models.IntegerField()       
    content = models.TextField()              
    # 포스터 이미지 넣기
    poster = models.ImageField(upload_to='posters/', null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)    