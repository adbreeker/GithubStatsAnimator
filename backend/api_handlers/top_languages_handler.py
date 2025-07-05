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
        - languages_count (optional): Number of languages to show, default 5
        - decimal_places (optional): Precision for percentages (0 for no floating point), default 1
        - count_other_languages (optional): Include "Other" category for remaining languages, default false
        - exclude_languages (optional): Comma-separated list of languages to exclude, default empty
        - width (optional): SVG width in pixels, default 400
        - height (optional): SVG height in pixels, default 300
        
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
            languages_count = int(request.args.get('languages_count', 5))
            decimal_places = int(request.args.get('decimal_places', 1))
            count_other_languages = request.args.get('count_other_languages', 'false').lower() == 'true'
            exclude_languages_str = request.args.get('exclude_languages', '')
            exclude_languages = [lang.strip() for lang in exclude_languages_str.split(',') if lang.strip()]
            width = int(request.args.get('width', 400))
            height = int(request.args.get('height', 300))
            
            # Validate parameters
            if theme not in ['light', 'dark']:
                return jsonify({
                    "error": "Invalid theme",
                    "message": "Theme must be 'light' or 'dark'",
                    "provided": theme
                }), 400
            
            if not (1 <= languages_count <= 20):
                return jsonify({
                    "error": "Invalid languages_count",
                    "message": "Languages count must be between 1 and 20",
                    "provided": languages_count
                }), 400
            
            if not (0 <= decimal_places <= 5):
                return jsonify({
                    "error": "Invalid decimal_places",
                    "message": "Decimal places must be between 0 and 5",
                    "provided": decimal_places
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
                    languages_count=languages_count,
                    decimal_places=decimal_places,
                    count_other_languages=count_other_languages,
                    exclude_languages=exclude_languages,
                    width=width,
                    height=height
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
