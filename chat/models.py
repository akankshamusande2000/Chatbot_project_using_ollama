from django.db import models
import uuid  
class ChatMessage(models.Model):
    session_id = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    user_message = models.TextField()
    bot_response = models.TextField(null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} - {self.timestamp}"
