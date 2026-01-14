from django.db import models
from django.utils import timezone
from apps.users.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField('제목', max_length=20)
    content = models.CharField('내용', max_length=20)
    region = models.CharField('지역', max_length=20)
    user = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    price = models.IntegerField('가격', default=1000)
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', null=True, blank=True)
    photo = models.ImageField('이미지', blank=True, upload_to='posts/%Y%m%d')
    nutrition_img = models.ImageField('영양성분이미지', blank=True, upload_to='posts/%Y%m%d')
    calorie = models.DecimalField('칼로리',default=100.0, max_digits=3, decimal_places=1)
    carbo = models.DecimalField('탄수화물', default=100.0, max_digits=3, decimal_places=1)
    protein = models.DecimalField('단백질', default=100.0,  max_digits=3, decimal_places=1)
    fat = models.DecimalField('지방', default=100.0,  max_digits=3, decimal_places=1)
    hashtag = models.CharField('해시태그', default='기타', max_length=20)

    def save(self, *args, **kwargs):
        if self.pk:  # 수정일 때에만 갱신
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)