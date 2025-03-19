from django.urls import path
from .views import chat_view, chat_page
from .views import export_chat_csv
urlpatterns = [
    path("chat/", chat_view, name="chat"),  
    path("", chat_page, name="chat_page"), 
    path("export/chat/csv/", export_chat_csv, name="export_chat_csv"),
    ]    

