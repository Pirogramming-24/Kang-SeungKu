from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# 1. 영화 정보 모델 (UI 입력 항목 반영)
class Movie(models.Model):
    # 장르 선택지 정의 (형님이 지정한 목록)
    GENRE_CHOICES = [
        ('ACTION', '액션'),
        ('ROMANCE', '로맨스/멜로'),
        ('SF', 'SF'),
        ('THRILLER', '스릴러'),
        ('DRAMA', '드라마'),
    ]

    # TMDB ID (TMDB 연동 영화인 경우 저장, 직접 등록은 null)
    tmdb_id = models.IntegerField(unique=True, verbose_name="TMDB ID", null=True, blank=True)
    
    # 1. 제목
    title = models.CharField(max_length=200, verbose_name="제목")
    
    # 2. 포스터 (TMDB URL과 직접 업로드 이미지 둘 다 고려)
    poster_path = models.CharField(max_length=200, verbose_name="포스터 경로(TMDB)", blank=True, null=True)
    poster_image = models.ImageField(upload_to='posters/', verbose_name="포스터 이미지(직접 업로드)", blank=True, null=True)
    
    # 3. 개봉년도 (UI 요청대로 '년도'만 정수로 저장)
    release_year = models.IntegerField(verbose_name="개봉년도", null=True, blank=True)
    
    # 4. 장르 (Dropdown 선택)
    genre = models.CharField(
        max_length=50, 
        choices=GENRE_CHOICES, 
        verbose_name="장르", 
        null=True, 
        blank=True
    )
    
    # 5. 감독 & 6. 주연배우
    director = models.CharField(max_length=100, verbose_name="감독", blank=True, null=True)
    actors = models.CharField(max_length=500, verbose_name="주연배우", help_text=",로 구분", blank=True, null=True)
    
    # 7. 러닝타임 (분 단위 입력)
    running_time = models.IntegerField(verbose_name="러닝타임(분)", null=True, blank=True)
    tmdb_average = models.FloatField(verbose_name="TMDB 평점", default=0.0)
    
    # ★ 러닝타임을 "0시간 00분" 형식으로 변환해주는 함수 (템플릿에서 사용)
    @property
    def running_time_display(self):
        if not self.running_time:
            return ""
        hours = self.running_time // 60
        minutes = self.running_time % 60
        return f"{hours}시간 {minutes}분"

    @property
    def star_list(self):
        # 1. 점수 결정 로직
        if self.tmdb_id: 
            # TMDB 영화라면: 10점 만점을 5점 만점으로 변환 (반올림)
            score = round(self.tmdb_average / 2)
        else:
            # 직접 추가한 영화라면: 연결된 리뷰의 평점을 가져옴
            review = self.reviews.first()
            score = review.rating if review else 0
        
        # 2. 별 리스트 생성 로직
        score = int(score) # 정수로 변환
        if score > 5: score = 5 # 안전장치
        
        stars = []
        for i in range(5):
            if i < score:
                stars.append('full')  # 채워진 별
            else:
                stars.append('empty') # 빈 별
        return stars
    
    def __str__(self):
        return self.title


# 2. 리뷰 모델
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', verbose_name="영화")
    
    # 8. 별점 (1~5점 선택지)
    RATING_CHOICES = [
        (1, '1점'),
        (2, '2점'),
        (3, '3점'),
        (4, '4점'),
        (5, '5점'),
    ]
    
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="별점",
        default=5
    )
    
    # 9. 리뷰 내용
    content = models.TextField(verbose_name="리뷰 내용")
    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    is_tmdb = models.BooleanField(default=False, verbose_name="TMDB 출처 여부")
    def __str__(self):
        return f"[{self.movie.title}] - {self.rating}점"