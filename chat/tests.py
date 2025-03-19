from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import ChatMessage

class ChatAPITestCase(TestCase):
    def setUp(self):
        """Setup test client and endpoint URL."""
        self.client = Client()
        self.chat_url = reverse("chat")  
    
    def test_chat_endpoint_valid_message(self):
        """Test sending a valid message to the chat endpoint."""
        response = self.client.post(
            self.chat_url,
            data=json.dumps({"message": "Hello, AI!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

    def test_chat_endpoint_empty_message(self):
        """Test sending an empty message."""
        response = self.client.post(
            self.chat_url,
            data=json.dumps({"message": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_chat_endpoint_invalid_method(self):
        """Test sending a GET request instead of POST."""
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 405)

    def test_chat_history_saved(self):
        """Test if messages are stored in the database."""
        message = "Test message"
        bot_response = "Test bot reply"
        ChatMessage.objects.create(
            session_id="test_session", user_message=message, bot_response=bot_response
        )
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.first().user_message, message)
