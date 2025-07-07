from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
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
            
            # Create a simple mock SVG instead of calling the complex generator
            mock_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0d1117"/>
  <text x="20" y="30" fill="#58a6ff" font-family="Arial" font-size="16" font-weight="bold">
    GitHub Stats for {username}
  </text>
  <text x="20" y="60" fill="#f0f6fc" font-family="Arial" font-size="14">
    ⭐ Stars: 123
  </text>
  <text x="20" y="85" fill="#f0f6fc" font-family="Arial" font-size="14">
    📝 Commits: 456
  </text>
  <text x="20" y="110" fill="#f0f6fc" font-family="Arial" font-size="14">
    🔀 Pull Requests: 78
  </text>
  <text x="20" y="135" fill="#f0f6fc" font-family="Arial" font-size="14">
    🐛 Issues: 90
  </text>
  <text x="20" y="170" fill="#7c3aed" font-family="Arial" font-size="12">
    Mock SVG - Replace with real data
  </text>
</svg>'''
            
            # Return SVG with proper headers
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(mock_svg.encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Simple SVG generation failed",
                "message": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
