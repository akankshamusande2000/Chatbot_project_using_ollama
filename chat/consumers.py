import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import get_ai_response, save_chat, get_chat_history  

# ChatConsumer with Context
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection."""
        self.session_id = str(uuid.uuid4())  
        self.chat_history = await get_chat_history(self.session_id) 
        await self.accept()

    async def receive(self, text_data):
        """Handles incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            user_message = data.get("message", "").strip()

            if not user_message:
                await self.send_error("Message cannot be empty.")
                return

            # Store the user message in the database
            await save_chat(self.session_id, user_message, None)

            # Send the user message and session ID to the AI model for context-aware response
            bot_reply = await get_ai_response(user_message, self.session_id)

            # Store the bot response in the database
            await save_chat(self.session_id, user_message, bot_reply)

            # Send bot response to the frontend
            await self.send(json.dumps({"response": bot_reply}))

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format.")
        except Exception as e:
            await self.send_error(f"An unexpected error occurred: {str(e)}")

    async def send_error(self, error_message):
        """Sends error messages to the frontend."""
        await self.send(json.dumps({"error": error_message}))
