from flask import Flask
from flask_cors import CORS
from app.routes import feedback_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(feedback_blueprint)
    
    return app