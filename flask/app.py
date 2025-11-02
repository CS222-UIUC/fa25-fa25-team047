from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post('/auth/login')
def login():
    payload = request.get_json(silent=True) or {}
    email = payload.get('email', '').strip()
    password = payload.get('password', '')

    if not email or '@' not in email:
        return (
            jsonify({'error': 'A valid email address is required.'}),
            400,
        )

    if not password or len(password) < 8:
        return (
            jsonify({'error': 'Password must be at least 8 characters long.'}),
            400,
        )

    token = f"dummy-session-{uuid4().hex}"
    return jsonify({'token': token, 'email': email})

@app.post('/api/chat')
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get('message', '').strip()
    conversation_history = payload.get('history', [])

    if not message:
        return jsonify({'error': 'Message is required.'}), 400

    try:
        # Prepare messages for OpenAI API
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        assistant_message = response.choices[0].message.content

        return jsonify({
            'message': assistant_message
        })
    
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return jsonify({'error': 'Failed to get response from AI.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
