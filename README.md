# Chatbot_project_using_ollama

A real-time AI-powered chatbot built with Django, WebSockets, and Ollama for natural language processing.

---

## Features

- **Real-time messaging:** WebSocket-based instant chat.
- **Session-based chat history:** Maintains conversation context per user session.
- **AI-generated responses:** Uses Ollama's `mistral` model for intelligent replies.
- **Database storage:** Saves chat history in PostgreSQL.
- **Rate limiting:** Prevents spam by restricting message frequency.
- **Chat export:** Download conversation history as CSV.

---

## Installation

### Step 1: Clone the Repository
```bash
(https://github.com/akankshamusande2000/Chatbot_project_using_ollama.git)
cd chatbot_project
```

### Step 2: Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project root and add the required configurations (e.g., database settings, API keys).

### Step 4: Apply Database Migrations
```bash
python manage.py migrate  
```

### Step 5: Start the Django Server
```bash
python manage.py runserver  
```

---

## API Endpoints

| Method | Endpoint            | Description |
|--------|---------------------|-------------|
| **POST**   | `/chat/`            | Sends a message and receives an AI response. |
| **GET**    | `/export/chat/csv/` | Exports chat history as a CSV file. |

---

## WebSocket Communication

To connect via WebSockets, use:
```
ws://your-domain/ws/chat/
```

---

## Technical Choices

### Why Django Channels instead of Flask-SocketIO?
- **Better WebSocket support:** Django Channels natively supports async WebSockets.
- **Scalability:** Can handle multiple users with ease.

### Why Ollama instead of OpenAI API?
- **Local processing:** Eliminates external API costs.
- **Faster responses:** Works offline for quick message generation.

### Why PostgreSQL instead of SQLite?
- **Scalability:** Handles concurrent users efficiently.
- **Reliability:** Better data integrity and storage.

---

## Limitations

- **Limited chat history retention** for performance optimization.
- **No multi-user authentication yet** 

---

## Future Enhancements

- **Multilingual support** 
- **Better UI/UX** 
- **Deployment on GCP Cloud Run** 
- **User authentication & profiles** 

---


