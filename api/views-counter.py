import sys
import os

# Add the current directory to Python path for local imports
sys.path.append(os.path.dirname(__file__))

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import asyncio
from utils.views_counter_generator import generate_views_counter_svg

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            user_agent = self.headers.get('User-Agent', '')
            theme = query_params.get('theme', ['dark'])[0]
            animated = query_params.get('animated', ['true'])[0].lower() == 'true'

            if theme not in ['light', 'dark']:
                raise ValueError(f"Invalid theme: {theme}")

            # Generate SVG
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            svg_content = loop.run_until_complete(generate_views_counter_svg(
                user_agent=user_agent, 
                theme=theme, 
                animated=animated
            ))

            loop.close()

            # Return SVG with proper headers
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(svg_content.encode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(str({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
