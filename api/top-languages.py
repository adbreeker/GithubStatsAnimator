import sys
import os

# Add the current directory to Python path for local imports
sys.path.append(os.path.dirname(__file__))

import json
import asyncio
from urllib.parse import parse_qs
from utils.top_languages_generator import create_top_languages_svg

def handler(request):
    # Handle CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    if request.method != 'GET':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Get username from environment
        username = os.getenv('GITHUB_USERNAME')
        if not username:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({
                    "error": "GitHub username not configured",
                    "message": "GITHUB_USERNAME environment variable is required"
                })
            }
        
        # Parse query parameters
        query_params = parse_qs(request.url.split('?', 1)[1] if '?' in request.url else '')
        
        # Get parameters with defaults
        theme = query_params.get('theme', ['dark'])[0]
        languages_count = int(query_params.get('languages_count', [5])[0])
        decimal_places = int(query_params.get('decimal_places', [1])[0])
        count_other_languages = query_params.get('count_other_languages', ['false'])[0].lower() == 'true'
        exclude_languages = query_params.get('exclude_languages', [''])[0].split(',') if query_params.get('exclude_languages', [''])[0] else []
        width = int(query_params.get('width', [400])[0])
        height = int(query_params.get('height', [300])[0])
        
        # Validate parameters
        if theme not in ['light', 'dark']:
            raise ValueError(f"Invalid theme: {theme}")
        
        if not (1 <= languages_count <= 20):
            raise ValueError(f"Invalid languages_count: {languages_count}")
        
        if not (0 <= decimal_places <= 5):
            raise ValueError(f"Invalid decimal_places: {decimal_places}")
        
        if not (200 <= width <= 1000):
            raise ValueError(f"Invalid width: {width}")
        
        if not (150 <= height <= 800):
            raise ValueError(f"Invalid height: {height}")
        
        # Generate SVG
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        svg_content = loop.run_until_complete(create_top_languages_svg(
            username=username,
            theme=theme,
            languages_count=languages_count,
            decimal_places=decimal_places,
            count_other_languages=count_other_languages,
            exclude_languages=exclude_languages,
            width=width,
            height=height
        ))
        
        loop.close()
        
        # Return SVG with proper headers
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/svg+xml',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
            },
            'body': svg_content
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                "error": "Invalid request parameters",
                "message": str(e)
            })
        }
