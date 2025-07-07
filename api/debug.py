from http.server import BaseHTTPRequestHandler
import json
import os
import sys

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Test if we can import the utils
            try:
                sys.path.append(os.path.dirname(__file__))
                from utils.account_general_generator import create_account_general_svg
                import_status = "SUCCESS: Utils imported successfully"
            except ImportError as e:
                import_status = f"IMPORT ERROR: {str(e)}"
            except Exception as e:
                import_status = f"OTHER ERROR: {str(e)}"
            
            # Get username from environment
            username = os.getenv('GITHUB_USERNAME', 'NOT_SET')
            
            response = {
                "function": "account-general-debug",
                "import_status": import_status,
                "github_username": username,
                "python_path": sys.path[-3:],  # Last 3 paths
                "current_dir": os.path.dirname(__file__),
                "utils_exists": os.path.exists(os.path.join(os.path.dirname(__file__), 'utils')),
                "utils_contents": os.listdir(os.path.join(os.path.dirname(__file__), 'utils')) if os.path.exists(os.path.join(os.path.dirname(__file__), 'utils')) else "NOT_FOUND"
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "error": "Debug function failed",
                "message": str(e),
                "type": type(e).__name__
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
