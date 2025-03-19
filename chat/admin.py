from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session_id", "user_message", "bot_response", "timestamp")
    search_fields = ("session_id", "user_message")

