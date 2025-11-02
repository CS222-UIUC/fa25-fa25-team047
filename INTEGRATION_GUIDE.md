# ChatGPT API Integration Guide

## Overview

The ChatGPT API has been successfully integrated into the chatbox application. The integration connects the React frontend to a Flask backend that communicates with OpenAI's GPT-4 model.

## Architecture

```
Frontend (React + TypeScript)
    ↓
Flask Backend (Python)
    ↓
OpenAI GPT-4 API
```

## Key Components

### Frontend
1. **`ChatContainer.tsx`** - Displays message history and loading states
2. **`ChatMessage.tsx`** - Individual message bubble component
3. **`PromptArea.tsx`** - Updated to handle message submission and display
4. **`api.ts`** - API client for communication with backend

### Backend
1. **`app.py`** - Flask server with `/api/chat` endpoint
2. **`requirements.txt`** - Python dependencies

## Setup Instructions

### 1. Backend Setup

```bash
cd flask
pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Run the server:
```bash
python app.py
```

Server runs on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd ChatBoxUI
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## Features

- ✅ Real-time chat with GPT-4
- ✅ Conversation history maintained across messages
- ✅ Loading indicators during API calls
- ✅ Error handling with toast notifications
- ✅ Message bubbles for user and assistant
- ✅ Auto-scroll to latest message
- ✅ File attachment support (UI ready)
- ✅ Modern UI with shadcn/ui components

## API Endpoints

### POST /api/chat

**Request:**
```json
{
  "message": "Create a problem about binary trees",
  "history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**
```json
{
  "message": "AI generated response..."
}
```

## Environment Variables

Required in `flask/.env`:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional in `.env` files:
- `VITE_API_URL` - Custom backend URL (defaults to http://localhost:5000)

## Testing

1. Start both servers
2. Login with any email and password (8+ chars)
3. Type a message in the chat
4. Verify AI response appears

## Troubleshooting

**Error: "Failed to get response from AI"**
- Check OpenAI API key is set correctly
- Verify API key has sufficient credits
- Check server logs for detailed error messages

**CORS errors**
- Ensure Flask server is running on port 5000
- Check CORS configuration in app.py

**Connection refused**
- Verify Flask server is running
- Check firewall settings

## Next Steps

Potential enhancements:
- Add support for code formatting in responses
- Implement streaming responses for real-time typing effect
- Add conversation persistence to database
- Enable file content extraction for attached files
- Add token usage tracking

