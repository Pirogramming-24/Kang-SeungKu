from django.db import models
from django.conf import settings 

class ChatHistory(models.Model):
    # 1. 누가 물어봤는지 (비회원이면 저장 안 함 -> null 허용 안 함, 무조건 유저 있어야 함)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 2. 어떤 기능을 썼는지 (sentiment, spam, ner, report)
    feature_name = models.CharField(max_length=50)
    
    # 3. 무엇을 물어봤는지
    user_input = models.TextField()
    
    # 4. AI가 뭐라고 했는지 (결과 전체를 JSON으로 저장하면 나중에 편함)
    ai_response = models.JSONField()
    
    # 5. 언제 했는지
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.feature_name}] {self.user.username} - {self.created_at}"