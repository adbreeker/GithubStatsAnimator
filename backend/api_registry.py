"""
API Registry
Central place to register all API routes
"""
from api_handlers.contribution_graph_handler import register_contribution_graph_routes

def register_all_routes(app):
    """Register all API routes with the Flask app"""
    
    # Register contribution graph routes
    register_contribution_graph_routes(app)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "healthy", "service": "github-stats-animator"}, 200
    
    # API info endpoint
    @app.route('/api/info', methods=['GET'])
    def api_info():
        return {
            "service": "GitHub Stats Animator Backend",
            "version": "1.0.0",
            "endpoints": [
                {
                    "path": "/api/contributions-graph",
                    "method": "GET",
                    "description": "Generate animated GitHub contribution graph",
                    "parameters": {
                        "theme": "light or dark (default: dark)",
                        "text": "Text to animate (default: ADBREEKER)", 
                        "animation_time": "Animation duration in seconds (default: 8.0)",
                        "pause_time": "Pause between cycles in seconds (default: 0.0)",
                        "line_color": "Color of eating lines in hex (default: #ff8c00)",
                        "line_alpha": "Transparency of lines 0.0-1.0 (default: 0.7)",
                        "square_size": "Size of contribution squares in pixels (default: 11)"
                    },
                    "note": "GitHub username is read from GITHUB_USERNAME environment variable"
                }
            ]
        }, 200
