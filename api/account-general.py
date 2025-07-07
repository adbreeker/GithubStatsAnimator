import sys
import os

# Add the current directory to Python path for local imports
sys.path.append(os.path.dirname(__file__))

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import asyncio
from utils.account_general_generator import create_account_general_svg

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
            
            # Available slot options
            slot_options = [
                'stars', 'commits_total', 'commits_year', 'pull_requests', 
                'code_reviews', 'issues', 'external_contributions'
            ]
            
            # Available icon options  
            icon_options = [
                'default', 'user', 'github', 'streak', 'default+github', 
                'default+streak', 'github+streak', 'user+github', 'user+streak', 'github+user'
            ]
            
            # Get parameters with defaults
            theme = query_params.get('theme', ['dark'])[0]
            icon = query_params.get('icon', ['default'])[0]
            slot1 = query_params.get('slot1', ['stars'])[0]
            slot2 = query_params.get('slot2', ['commits_total'])[0]
            slot3 = query_params.get('slot3', ['commits_year'])[0]
            slot4 = query_params.get('slot4', ['pull_requests'])[0]
            slot5 = query_params.get('slot5', ['issues'])[0]
            
            # Validate parameters
            if theme not in ['light', 'dark']:
                raise ValueError(f"Invalid theme: {theme}")
            
            if icon not in icon_options:
                raise ValueError(f"Invalid icon: {icon}")
            
            for slot_name, slot_value in [('slot1', slot1), ('slot2', slot2), ('slot3', slot3), ('slot4', slot4), ('slot5', slot5)]:
                if slot_value not in slot_options:
                    raise ValueError(f"Invalid {slot_name}: {slot_value}")
            
            # Generate SVG
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            svg_content = loop.run_until_complete(create_account_general_svg(
                username=username,
                theme=theme,
                icon=icon,
                slot1=slot1,
                slot2=slot2,
                slot3=slot3,
                slot4=slot4,
                slot5=slot5
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
