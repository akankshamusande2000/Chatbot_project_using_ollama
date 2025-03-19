import ollama
from .models import ChatMessage
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

# AI RESPONSE HANDLER with Context
async def get_ai_response(user_input, session_id):
    """Generates AI response using Ollama with context from previous messages."""
    try:
        chat_history = await get_chat_history(session_id)
        max_context_size = 3
        chat_history = chat_history[-max_context_size:]

        messages = [{"role": "system", "content": "Provide factual, verifiable answers."}]
        
        for chat in chat_history:
            messages.append({"role": "user", "content": chat["user_message"]})
            if chat["bot_response"]:
                messages.append({"role": "assistant", "content": chat["bot_response"]})

        messages.append({"role": "user", "content": user_input})

        response = await sync_to_async(ollama.chat)(
            model="mistral",
            messages=messages,
            options={"num_keep":100, "num_predict":100}  
        )

        if response and "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        return "Sorry, I couldn't generate a response."
    except Exception as e:
        logger.error(f"AI Service Error: {str(e)}")
        return "Sorry, I couldn't generate a response."

# SAVE MESSAGE TO DATABASE
@sync_to_async
def save_chat(session_id, user_message, bot_response):
    """Saves user & bot messages to the database asynchronously."""
    try:
        if not bot_response:
            bot_response = "Sorry, no response from bot."

        ChatMessage.objects.create(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response
        )
    except Exception as e:
        logger.error(f"Database Error: {str(e)}")  

# RETRIEVE CHAT HISTORY
@sync_to_async
def get_chat_history(session_id):
    """Retrieves chat history for a session."""
    return list(ChatMessage.objects.filter(session_id=session_id).order_by("timestamp").values("timestamp", "user_message", "bot_response"))

# FORMAT CHAT DATA FOR EXPORT
def format_chat_data(chat_history, format_type):
    """Formats chat data based on export type."""
    try:
        if format_type == "csv":
            return [["Timestamp", "User Message", "Bot Response"]] + [
                [chat["timestamp"], chat["user_message"], chat["bot_response"]]
                for chat in chat_history
            ]
    except Exception as e:
        logger.error(f"Formatting Error: {str(e)}")
        return None
