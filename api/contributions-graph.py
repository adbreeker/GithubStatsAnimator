import sys
import os

# Add the current directory to Python path for local imports
sys.path.append(os.path.dirname(__file__))

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import asyncio
from utils.contributions_graph_generator import generate_contributions_svg

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get username from environment
            username = os.getenv('GITHUB_USERNAME')
            if not username:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "GitHub username not configured",
                    "message": "GITHUB_USERNAME environment variable is required"
                }).encode())
                return
            
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
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(svg_content.encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Invalid request parameters",
                "message": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
