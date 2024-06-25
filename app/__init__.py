import logging
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'development':
        # Use Flask-CORS to handle CORS
        CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}},
             supports_credentials=True)
    
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)

    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
