"""
GitHub Stats Animator Backend
Main application entry point
"""
from flask import Flask
from flask_cors import CORS
from api_registry import register_all_routes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Register all API routes
    register_all_routes(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    # Get configuration from environment
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"Starting GitHub Stats Animator Backend...")
    print(f"Debug mode: {debug_mode}")
    print(f"Server running on http://{host}:{port}")
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port
    )
