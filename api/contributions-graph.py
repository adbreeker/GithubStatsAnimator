import sys
import os

# Add the current directory to Python path for local imports
sys.path.append(os.path.dirname(__file__))

import json
import asyncio
from urllib.parse import parse_qs
from utils.contributions_graph_generator import generate_contributions_svg

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
        text = query_params.get('text', ['ADBREEKER'])[0]
        animation_time = float(query_params.get('animation_time', [8.0])[0])
        pause_time = float(query_params.get('pause_time', [0.0])[0])
        line_color = query_params.get('line_color', ['#ff8c00'])[0]
        line_alpha = float(query_params.get('line_alpha', [0.7])[0])
        square_size = int(query_params.get('square_size', [11])[0])
        
        # Validate parameters
        if theme not in ['light', 'dark']:
            raise ValueError(f"Invalid theme: {theme}")
        
        if not (0.0 <= line_alpha <= 1.0):
            raise ValueError(f"Invalid line_alpha: {line_alpha}")
        
        if square_size < 1 or square_size > 30:
            raise ValueError(f"Invalid square_size: {square_size}")
        
        # Generate SVG
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        svg_content = loop.run_until_complete(generate_contributions_svg(
            username=username,
            theme=theme,
            text=text,
            animation_time=animation_time,
            pause_time=pause_time,
            line_color=line_color,
            line_alpha=line_alpha,
            square_size=square_size
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
