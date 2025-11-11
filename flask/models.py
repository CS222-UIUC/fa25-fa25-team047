from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    submissions = db.relationship('Submission', back_populates='user', lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<User {self.email}>'


class Problem(db.Model):
    """Problem model for coding challenges."""
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    topic = db.Column(db.String(100), nullable=False)  # e.g., "dynamic programming", "trees"

    # Function signature and starter code
    function_signature = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=True)

    # Test cases
    sample_test_cases = db.Column(db.JSON, nullable=False)  # Public test cases shown to user
    hidden_test_cases = db.Column(db.JSON, nullable=False)  # Hidden edge cases

    # Solution for reference
    solution = db.Column(db.Text, nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_published = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    submissions = db.relationship('Submission', back_populates='problem', lazy=True)

    def to_dict(self, include_hidden=False):
        """Convert problem to dictionary."""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'function_signature': self.function_signature,
            'starter_code': self.starter_code,
            'sample_test_cases': self.sample_test_cases,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
        }
        if include_hidden:
            data['hidden_test_cases'] = self.hidden_test_cases
            data['solution'] = self.solution
        return data

    def __repr__(self):
        return f'<Problem {self.title}>'


class Submission(db.Model):
    """Submission model for tracking user code submissions."""
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)

    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False, default='python')

    # Results
    status = db.Column(db.String(50), nullable=False)  # e.g., "passed", "failed", "error"
    test_results = db.Column(db.JSON, nullable=True)  # Detailed test case results
    execution_time = db.Column(db.Float, nullable=True)  # in seconds

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='submissions')
    problem = db.relationship('Problem', back_populates='submissions')

    def to_dict(self):
        """Convert submission to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'code': self.code,
            'language': self.language,
            'status': self.status,
            'test_results': self.test_results,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'
