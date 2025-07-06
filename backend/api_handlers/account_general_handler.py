"""
Account General Stats API Handler
Handles endpoints related to GitHub account general statistics visualization
"""
from flask import request, jsonify, Response
import asyncio
import os
from utils.account_general_generator import create_account_general_svg

def register_account_general_routes(app):
    """Register account general stats related routes"""
    
    @app.route('/api/account-general', methods=['GET'])
    def get_account_general():
        """
        Generate GitHub account general stats SVG
        
        Query Parameters:
        - icon (optional): 'default', 'github', 'streak', or 'default+github', 'default+streak', 'github+streak', default 'default'
        - slot1 (optional): 'stars', 'commits_total', 'commits_year', 'pull_requests', 'code_reviews', 'issues', 'external_contributions', default 'stars'
        - slot2 (optional): Same options as slot1, default 'commits_total'
        - slot3 (optional): Same options as slot1, default 'commits_year'
        - slot4 (optional): Same options as slot1, default 'pull_requests'
        - slot5 (optional): Same options as slot1, default 'issues'
        - theme (optional): 'light' or 'dark', default 'dark'
        
        Note: GitHub username is read from environment variables (GITHUB_USERNAME)
        Fixed size: 400x200 pixels for compact layout with title and stats on left, logo on right
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
            
            # Get optional parameters with defaults
            icon = request.args.get('icon', 'default')
            slot1 = request.args.get('slot1', 'stars')
            slot2 = request.args.get('slot2', 'commits_total')
            slot3 = request.args.get('slot3', 'commits_year')
            slot4 = request.args.get('slot4', 'pull_requests')
            slot5 = request.args.get('slot5', 'issues')
            theme = request.args.get('theme', 'dark')
            
            # Validate parameters
            if theme not in ['light', 'dark']:
                return jsonify({
                    "error": "Invalid theme",
                    "message": f"Theme must be 'light' or 'dark', got '{theme}'"
                }), 400
                
            if icon not in icon_options:
                return jsonify({
                    "error": "Invalid icon",
                    "message": f"Icon must be one of {icon_options}, got '{icon}'"
                }), 400
            
            # Validate slot parameters
            slots = [slot1, slot2, slot3, slot4, slot5]
            for i, slot in enumerate(slots, 1):
                if slot not in slot_options:
                    return jsonify({
                        "error": f"Invalid slot{i}",
                        "message": f"slot{i} must be one of {slot_options}, got '{slot}'"
                    }), 400
            
            # Generate SVG using asyncio (fixed 500x300 dimensions)
            try:
                svg_content = asyncio.run(create_account_general_svg(
                    username=username,
                    icon=icon,
                    slots=slots,
                    theme=theme
                ))
                
                return Response(
                    svg_content,
                    mimetype='image/svg+xml',
                    headers={
                        'Cache-Control': 'public, max-age=1800',  # 30 minutes cache
                        'Content-Type': 'image/svg+xml; charset=utf-8'
                    }
                )
                
            except Exception as e:
                error_msg = str(e)
                if "not found" in error_msg.lower():
                    return jsonify({
                        "error": "User not found",
                        "message": f"GitHub user '{username}' not found",
                        "hint": "Check if the GITHUB_USERNAME is correct"
                    }), 404
                elif "rate limit" in error_msg.lower():
                    return jsonify({
                        "error": "Rate limit exceeded",
                        "message": "GitHub API rate limit exceeded. Please try again later.",
                        "hint": "Make sure GITHUB_TOKEN is set for higher rate limits"
                    }), 429
                else:
                    return jsonify({
                        "error": "SVG generation failed",
                        "message": error_msg,
                        "hint": "Check your GitHub token and username configuration"
                    }), 500
                    
        except ValueError as e:
            return jsonify({
                "error": "Invalid parameter",
                "message": str(e)
            }), 400
        except Exception as e:
            return jsonify({
                "error": "Internal server error",
                "message": str(e)
            }), 500
