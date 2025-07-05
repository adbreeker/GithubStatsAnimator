"""
API Registry
Central place to register all API routes
"""
from api_handlers.contributions_graph_handler import register_contributions_graph_routes
from api_handlers.top_languages_handler import register_top_languages_routes

def register_all_routes(app):
    """Register all API routes with the Flask app"""

    # Register contributions graph routes
    register_contributions_graph_routes(app)
    
    # Register top languages routes
    register_top_languages_routes(app)
    
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
                    "description": "Generate animated GitHub contributions graph",
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
                },
                {
                    "path": "/api/top-languages",
                    "method": "GET",
                    "description": "Generate GitHub top languages SVG chart",
                    "parameters": {
                        "theme": "light or dark (default: dark)",
                        "limit": "Number of languages to show 1-20 (default: 5)",
                        "width": "SVG width in pixels 200-1000 (default: 400)",
                        "height": "SVG height in pixels 150-800 (default: 300)",
                        "show_percentages": "Show percentage labels true/false (default: true)",
                        "title": "Custom title (default: Most Used Languages)"
                    },
                    "note": "GitHub username is read from GITHUB_USERNAME environment variable"
                }
            ]
        }, 200
