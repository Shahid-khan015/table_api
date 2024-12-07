from flask import Flask
from flask_cors import CORS
from config import Config
from routes.video_routes import video_bp
from routes.health_routes import health_bp
from error_handlers import register_error_handlers

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(video_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()