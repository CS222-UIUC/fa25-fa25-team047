# ChatGPT Integration Setup Guide

## Quick Start

### Prerequisites
- Node.js (v18+)
- Python 3.8+
- OpenAI API Key

### 1. Backend Setup

```bash
cd flask
pip install -r requirements.txt
```

Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

Start the Flask server:
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

### 3. Usage

1. Open `http://localhost:3000` in your browser
2. Login with any email and password (8+ characters)
3. Start chatting with the AI!

## Project Structure

```
.
├── flask/
│   ├── app.py              # Backend with OpenAI integration
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
├── ChatBoxUI/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatContainer.tsx  # Message display
│   │   │   ├── ChatMessage.tsx    # Individual messages
│   │   │   ├── PromptArea.tsx     # Chat input
│   │   │   └── ...
│   │   ├── lib/
│   │   │   └── api.ts             # API client
│   │   └── App.tsx               # Main app
│   └── package.json
└── INTEGRATION_GUIDE.md    # Detailed integration docs
```

## Key Features

✅ Real-time chat with GPT-4  
✅ Conversation history  
✅ Loading indicators  
✅ Error handling  
✅ Modern UI  
✅ File attachment UI  

## Troubleshooting

**Port already in use:**
- Backend: Change port in `flask/app.py` (line 86)
- Frontend: Change port in `ChatBoxUI/vite.config.ts`

**API errors:**
- Verify OpenAI API key is set correctly
- Check server logs for detailed errors

**CORS errors:**
- Ensure Flask server is running
- Check CORS config in `flask/app.py`

## Next Steps

- Add streaming responses for real-time typing
- Implement conversation persistence
- Add code syntax highlighting
- Enable file content processing

