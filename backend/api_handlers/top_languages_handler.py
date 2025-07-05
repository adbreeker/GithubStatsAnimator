"""
Top Languages API Handler
Handles endpoints related to GitHub top languages visualization
"""
from flask import request, jsonify, Response
import asyncio
import os
from utils.top_languages_generator import create_top_languages_svg

def register_top_languages_routes(app):
    """Register top languages related routes"""
    
    @app.route('/api/top-languages', methods=['GET'])
    def get_top_languages():
        """
        Generate GitHub top languages SVG chart
        
        Query Parameters:
        - theme (optional): 'light' or 'dark', default 'dark'
        - limit (optional): Number of languages to show, default 5
        - width (optional): SVG width in pixels, default 400
        - height (optional): SVG height in pixels, default 300
        - show_percentages (optional): Show percentage labels, default true
        - title (optional): Custom title, default 'Most Used Languages'
        
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
            limit = int(request.args.get('limit', 5))
            width = int(request.args.get('width', 400))
            height = int(request.args.get('height', 300))
            show_percentages = request.args.get('show_percentages', 'true').lower() == 'true'
            title = request.args.get('title', 'Most Used Languages')
            
            # Validate parameters
            if theme not in ['light', 'dark']:
                return jsonify({
                    "error": "Invalid theme",
                    "message": "Theme must be 'light' or 'dark'",
                    "provided": theme
                }), 400
            
            if not (1 <= limit <= 20):
                return jsonify({
                    "error": "Invalid limit",
                    "message": "Limit must be between 1 and 20",
                    "provided": limit
                }), 400
            
            if not (200 <= width <= 1000):
                return jsonify({
                    "error": "Invalid width",
                    "message": "Width must be between 200 and 1000 pixels",
                    "provided": width
                }), 400
            
            if not (150 <= height <= 800):
                return jsonify({
                    "error": "Invalid height",
                    "message": "Height must be between 150 and 800 pixels",
                    "provided": height
                }), 400
            
            # Generate SVG asynchronously
            try:
                svg_content = asyncio.run(create_top_languages_svg(
                    username=username,
                    theme=theme,
                    limit=limit,
                    width=width,
                    height=height,
                    show_percentages=show_percentages,
                    title=title
                ))
                
                # Return SVG with proper content type
                return Response(
                    svg_content,
                    mimetype='image/svg+xml',
                    headers={
                        'Content-Disposition': f'inline; filename="{username}_top_languages.svg"',
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
