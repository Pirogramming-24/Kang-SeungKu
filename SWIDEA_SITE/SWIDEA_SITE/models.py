from django.db import models
from django.contrib.auth.models import User 

class DevTool(models.Model):
    name = models.CharField('이름', max_length=50)
    kind = models.CharField('종류', max_length=50)
    content = models.TextField('설명')
    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField('아이디어명', max_length=50)
    image = models.ImageField('이미지', upload_to='ideas/', blank=True, null=True)
    content = models.TextField('아이디어 설명')
    interest = models.IntegerField('아이디어 관심도', default=0) 
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, verbose_name='예상 개발툴')
    created_date = models.DateTimeField('작성일', auto_now_add=True)
    updated_date = models.DateTimeField('수정일', auto_now=True)
    def __str__(self):
        return self.title
class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')
    
    class Meta:
        unique_together = ('idea', 'user')