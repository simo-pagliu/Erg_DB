from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Determine the environment and load the corresponding configuration
    env = os.getenv('FLASK_ENV', 'development')
    from .config import config_by_name
    app.config.from_object(config_by_name[env])

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import models and routes here to avoid circular imports
        from . import models
        from .routes import api_bp
        from .coach import coach_bp        

        # Register Blueprint
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(coach_bp, url_prefix='/coach')

        # (optional) Create tables only if needed for initial setup
        if env == 'development':
            db.create_all()

    return app
