#!/usr/bin/env python3
"""
Local Development Server
Simulates Vercel serverless functions for local testing
"""
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import importlib.util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LocalDevHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Route to appropriate API function
        if path.startswith('/api/'):
            endpoint = path[5:]  # Remove '/api/' prefix
            self.handle_api_request(endpoint)
        else:
            # Serve frontend files (for full-stack testing)
            self.serve_frontend()
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_api_request(self, endpoint):
        """Handle API requests by importing and calling the appropriate function"""
        try:
            # Map endpoints to their corresponding files
            endpoint_map = {
                'health': 'api/health.py',
                'account-general': 'api/account-general.py',
                'top-languages': 'api/top-languages.py',
                'contributions-graph': 'api/contributions-graph.py',
                'views-counter': 'api/views-counter.py'
            }
            
            if endpoint not in endpoint_map:
                self.send_error(404, f"Endpoint not found: {endpoint}")
                return
            
            # Import the module dynamically
            module_path = endpoint_map[endpoint]
            spec = importlib.util.spec_from_file_location("handler_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Create a temporary handler instance to access the logic
            # We'll inherit from the module's handler class and override the socket-related methods
            class LocalHandler(module.handler):
                def __init__(self, parent_handler):
                    # Don't call super().__init__ to avoid socket setup
                    self.path = parent_handler.path
                    self.headers = parent_handler.headers
                    self.command = parent_handler.command
                    self.parent = parent_handler
                
                def send_response(self, code, message=None):
                    return self.parent.send_response(code, message)
                
                def send_header(self, keyword, value):
                    return self.parent.send_header(keyword, value)
                
                def end_headers(self):
                    return self.parent.end_headers()
                
                @property
                def wfile(self):
                    return self.parent.wfile
            
            # Create the handler and call the method
            handler = LocalHandler(self)
            handler.do_GET()
            
        except Exception as e:
            print(f"Error handling {endpoint}: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def serve_frontend(self):
        """Serve frontend files for testing"""
        # Simple redirect to frontend development server
        self.send_response(302)
        self.send_header('Location', 'http://localhost:5173')  # Vite default port
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to provide better logging"""
        print(f"[{self.date_time_string()}] {format % args}")

def main():
    """Start the local development server"""
    port = int(os.getenv('DEV_PORT', 8000))
    host = os.getenv('DEV_HOST', 'localhost')
    
    print(f"Starting Local Development Server...")
    print(f"Server: http://{host}:{port}")
    print(f"API Base: http://{host}:{port}/api/")
    print(f"Available endpoints:")
    print(f"   - http://{host}:{port}/api/health")
    print(f"   - http://{host}:{port}/api/account-general")
    print(f"   - http://{host}:{port}/api/top-languages")
    print(f"   - http://{host}:{port}/api/contributions-graph")
    print(f"\nMake sure to run your frontend dev server on http://localhost:5173")
    print(f"Environment: {os.getenv('GITHUB_USERNAME', 'Not set')}")
    print(f"\nPress Ctrl+C to stop\n")
    
    server = HTTPServer((host, port), LocalDevHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\nShutting down development server...")
        server.server_close()

if __name__ == '__main__':
    main()
