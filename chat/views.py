from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import async_to_sync
from .services import get_ai_response, save_chat
import csv
from .models import ChatMessage
from django_ratelimit.decorators import ratelimit

@csrf_exempt
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def chat_view(request):
    """Handles user messages and AI responses, maintaining session context"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        user_input = data.get("message", "").strip()

        if not user_input:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        # Ensure session exists
        session_id = ensure_session(request)

        # Retrieve existing chat history from session
        chat_history = request.session.get("chat_history", [])

        # Get AI response and save chat
        bot_response = async_to_sync(get_ai_response)(user_input, session_id)
        save_chat(session_id, user_input, bot_response)

        # Append messages to session chat history
        chat_history.append({"user": user_input, "bot": bot_response})
        request.session["chat_history"] = chat_history  

        return JsonResponse({"response": bot_response, "history": chat_history})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except KeyError:
        return JsonResponse({"error": "Missing required data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

def ensure_session(request):
    """Ensures session exists, creates a new one if necessary."""
    if not request.session.session_key:
        request.session.create()
        request.session["chat_history"] = [] 
    return request.session.session_key


def chat_page(request):
    """Renders the chat interface"""
    return render(request, "chat/chat.html")


def export_chat_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="chat_messages.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "User", "Message", "Timestamp"])

    chats = ChatMessage.objects.all()
    for chat in chats:
        writer.writerow([chat.id, chat.session_id, chat.user_message, chat.bot_response, chat.timestamp])


    return response