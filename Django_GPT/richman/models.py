from django.db import models
from django.conf import settings 

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    feature_name = models.CharField(max_length=50)
    
    user_input = models.TextField()
    
    ai_response = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.feature_name}] {self.user.username} - {self.created_at}"