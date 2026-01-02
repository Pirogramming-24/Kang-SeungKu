from django.db import models
# 찜하기 기능을 위해 User 모델을 가져옵니다.
from django.contrib.auth.models import User 

class DevTool(models.Model):
    name = models.CharField('이름', max_length=50)
    kind = models.CharField('종류', max_length=50)
    content = models.TextField('설명')


class Idea(models.Model):
    title = models.CharField('아이디어명', max_length=50)
    image = models.ImageField('이미지', upload_to='ideas/', blank=True, null=True)
    content = models.TextField('아이디어 설명')
    interest = models.IntegerField('아이디어 관심도', default=0) # 초기값 0
    # DevTool과 연결 (Requirement 5: devtool은 리스트 항목 중에서 선택)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, verbose_name='예상 개발툴')
    created_date = models.DateTimeField('작성일', auto_now_add=True)
    updated_date = models.DateTimeField('수정일', auto_now=True)

# [NEW] 찜하기 기능을 위한 모델 (IdeaStar)
class IdeaStar(models.Model):
    # 어떤 아이디어인지
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')
    # 누가 찜했는지 (로그인 기능이 있다고 가정)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')
    
    class Meta:
        # 한 유저가 같은 아이디어를 중복해서 찜할 수 없게 막음
        unique_together = ('idea', 'user')