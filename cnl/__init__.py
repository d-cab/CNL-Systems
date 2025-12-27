import os
from flask import Flask
from dotenv import load_dotenv
from cnl.extensions import db
from cnl.routes import register_blueprints

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Base directory paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/salon.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        ADMIN_USERNAME=os.getenv("ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD", "password"),
    )

    # Initialize extensions properly
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app