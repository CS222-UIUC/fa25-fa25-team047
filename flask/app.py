from flask import Flask, jsonify, request
from flask_cors import CORS
from config import config
from models import db, User, Problem
from auth import generate_token, token_required
import os

def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Routes
    @app.route('/')
    def hello_world():
        return jsonify({'message': 'Code Companion API', 'version': '1.0.0'})

    @app.route('/auth/register', methods=['POST'])
    def register():
        """Register a new user."""
        try:
            payload = request.get_json(silent=True) or {}
            email = payload.get('email', '').strip().lower()
            password = payload.get('password', '')

            # Validation
            if not email or '@' not in email:
                return jsonify({'error': 'A valid email address is required.'}), 400

            if not password or len(password) < 8:
                return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'An account with this email already exists.'}), 409

            # Create new user
            user = User(email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Generate token
            token = generate_token(user.id, user.email)

            return jsonify({
                'message': 'User registered successfully',
                'token': token,
                'user': user.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Registration error: {str(e)}')
            return jsonify({'error': 'An error occurred during registration.'}), 500

    @app.route('/auth/login', methods=['POST'])
    def login():
        """Authenticate a user and return a token."""
        try:
            payload = request.get_json(silent=True) or {}
            email = payload.get('email', '').strip().lower()
            password = payload.get('password', '')

            # Validation
            if not email or '@' not in email:
                return jsonify({'error': 'A valid email address is required.'}), 400

            if not password:
                return jsonify({'error': 'Password is required.'}), 400

            # Find user
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return jsonify({'error': 'Invalid email or password.'}), 401

            # Generate token
            token = generate_token(user.id, user.email)

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }), 200

        except Exception as e:
            app.logger.error(f'Login error: {str(e)}')
            return jsonify({'error': 'An error occurred during login.'}), 500

    @app.route('/auth/me', methods=['GET'])
    @token_required
    def get_current_user(current_user):
        """Get the current authenticated user's information."""
        return jsonify({'user': current_user.to_dict()}), 200

    @app.route('/problems', methods=['GET'])
    @token_required
    def get_problems(current_user):
        """Get all published problems."""
        try:
            # Query parameters for filtering
            difficulty = request.args.get('difficulty')
            topic = request.args.get('topic')

            query = Problem.query.filter_by(is_published=True)

            if difficulty:
                query = query.filter_by(difficulty=difficulty.lower())

            if topic:
                query = query.filter_by(topic=topic.lower())

            problems = query.all()
            return jsonify({
                'problems': [p.to_dict() for p in problems],
                'count': len(problems)
            }), 200

        except Exception as e:
            app.logger.error(f'Error fetching problems: {str(e)}')
            return jsonify({'error': 'An error occurred while fetching problems.'}), 500

    @app.route('/problems/<int:problem_id>', methods=['GET'])
    @token_required
    def get_problem(current_user, problem_id):
        """Get a specific problem by ID."""
        problem = Problem.query.get(problem_id)

        if not problem or not problem.is_published:
            return jsonify({'error': 'Problem not found.'}), 404

        return jsonify({'problem': problem.to_dict()}), 200

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
