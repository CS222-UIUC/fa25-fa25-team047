from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

#login page

app = Flask(__name__)
CORS(app, resources={r"/auth/*": {"origins": "*"}})

    # Load configuration
    app.config.from_object(config[config_name])

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

if __name__ == '__main__':
    app.run(debug=True)
