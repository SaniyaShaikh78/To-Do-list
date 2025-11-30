from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'your-secret-key'  # change in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    # Import and register blueprints here to avoid circular imports
    from app.routes.tasks import tasks_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
