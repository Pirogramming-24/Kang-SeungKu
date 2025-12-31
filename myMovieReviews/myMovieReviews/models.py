from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Review(models.Model) :
    
    GENRE_CHOICES = [
        ('ACTION', '액션'),
        ('ROMANCE', '로맨스'),
        ('COMEDY', '코미디'),
        ('THRILLER', '스릴러'),
        ('DRAMA', '드라마'),
        ('SF', 'SF'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="제목")
    release_year = models.IntegerField(verbose_name="개봉년도")
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, verbose_name="장르")
    rating = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        verbose_name="별점",
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )

    running_time = models.IntegerField(verbose_name="러닝타임")
    content = models.TextField(verbose_name="리뷰 내용")
    director = models.CharField(max_length=100, verbose_name="감독")
    actors = models.CharField(max_length=200, verbose_name="주연")           
    # 포스터 이미지 넣기
    poster = models.ImageField(upload_to='posters/', null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)    