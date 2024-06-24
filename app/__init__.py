from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'development':
        # Restrict CORS to specific origin and allow headers
        CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}},
             supports_credentials=True)

    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
