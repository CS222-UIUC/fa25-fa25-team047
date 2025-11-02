# Flask Backend - ChatGPT Integration

## Setup

1. **Install dependencies:**
   ```bash
   cd flask
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `flask` directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Flask server:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /api/chat

Send a chat message and get AI response.

**Request body:**
```json
{
  "message": "Your message here",
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
  "message": "AI response"
}
```

### POST /auth/login

User authentication endpoint.

## CORS

The app is configured to allow CORS from all origins for development. Adjust this in production.

