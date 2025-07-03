"""
Contribution Graph API Handler
Handles all endpoints related to GitHub contribution graph generation
"""
from flask import request, jsonify, Response
import asyncio
import os
from utils.github_svg_generator import generate_contributions_svg

def register_contribution_graph_routes(app):
    """Register contribution graph related routes"""
    
    @app.route('/api/contribution-graph', methods=['GET'])
    def get_contribution_graph():
        """
        Generate animated GitHub contribution graph SVG
        
        Query Parameters:
        - theme (optional): 'light' or 'dark', default 'dark'
        - text (optional): Text to animate, default 'ADBREEKER'
        - animation_time (optional): Animation duration in seconds, default 8.0
        - pause_time (optional): Pause between cycles in seconds, default 0.0
        - line_color (optional): Hex color for eating lines, default '#ff8c00'
        - line_alpha (optional): Line transparency 0.0-1.0, default 0.7
        - square_size (optional): Square size in pixels, default 11
        
        Note: GitHub username is read from environment variables (GITHUB_USERNAME)
        """
        try:
            # Get username from environment
            username = os.getenv('GITHUB_USERNAME')
            if not username:
                return jsonify({
                    "error": "GitHub username not configured",
                    "message": "GITHUB_USERNAME environment variable is required",
                    "hint": "Set GITHUB_USERNAME in your .env file"
                }), 500
            
            # Get optional parameters with defaults
            theme = request.args.get('theme', 'dark')
            text = request.args.get('text', 'ADBREEKER')
            animation_time = float(request.args.get('animation_time', 8.0))
            pause_time = float(request.args.get('pause_time', 0.0))
            line_color = request.args.get('line_color', '#ff8c00')
            line_alpha = float(request.args.get('line_alpha', 0.7))
            square_size = int(request.args.get('square_size', 11))
            
            # Validate parameters
            if theme not in ['light', 'dark']:
                return jsonify({
                    "error": "Invalid theme",
                    "message": "Theme must be 'light' or 'dark'",
                    "provided": theme
                }), 400
            
            if not (0.0 <= line_alpha <= 1.0):
                return jsonify({
                    "error": "Invalid line_alpha",
                    "message": "line_alpha must be between 0.0 and 1.0",
                    "provided": line_alpha
                }), 400
            
            if not (1 <= square_size <= 50):
                return jsonify({
                    "error": "Invalid square_size", 
                    "message": "square_size must be between 1 and 50 pixels",
                    "provided": square_size
                }), 400
            
            if not line_color.startswith('#') or len(line_color) not in [4, 7]:
                return jsonify({
                    "error": "Invalid line_color",
                    "message": "line_color must be a valid hex color (e.g., #ff8c00 or #f80)",
                    "provided": line_color
                }), 400
            
            # Generate SVG asynchronously
            try:
                svg_content = asyncio.run(generate_contributions_svg(
                    username=username,
                    theme=theme,
                    text=text,
                    line_color=line_color,
                    line_alpha=line_alpha,
                    square_size=square_size,
                    animation_time=animation_time,
                    pause_time=pause_time
                ))
                
                # Return SVG with proper content type
                return Response(
                    svg_content,
                    mimetype='image/svg+xml',
                    headers={
                        'Content-Disposition': f'inline; filename="{username}_contributions.svg"',
                        'Cache-Control': 'no-cache'
                    }
                )
                
            except Exception as svg_error:
                return jsonify({
                    "error": "SVG generation failed",
                    "message": str(svg_error),
                    "username": username
                }), 500
                
        except ValueError as ve:
            return jsonify({
                "error": "Invalid parameter value",
                "message": str(ve)
            }), 400
            
        except Exception as e:
            return jsonify({
                "error": "Internal server error",
                "message": str(e)
            }), 500
