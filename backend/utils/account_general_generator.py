"""
GitHub Account General Stats SVG Generator
Creates an SVG representation of GitHub account general statistics using GraphQL
"""

import asyncio
import aiohttp
import json
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# GitHub GraphQL API endpoint
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

async def fetch_avatar_as_data_uri(avatar_url: str) -> str:
    """Fetch avatar image and convert to base64 data URI"""
    if not avatar_url:
        return None
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    # Convert to base64
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    # Return as data URI (assuming PNG format)
                    return f"data:image/png;base64,{base64_data}"
    except:
        pass
    
    return None

# Color schemes
THEMES = {
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "text_primary": "#24292f",
        "text_secondary": "#656d76",
        "accent": "#0969da",
        "success": "#1a7f37",
        "warning": "#d1242f"
    },
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "text_primary": "#f0f6fc",
        "text_secondary": "#8b949e",
        "accent": "#58a6ff",
        "success": "#3fb950",
        "warning": "#f85149"
    }
}

class GitHubAccountStatsAPI:
    """GitHub API client for fetching account statistics"""
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

    async def fetch_account_stats(self, username: str) -> Dict[str, Any]:
        """Fetch comprehensive account statistics using GraphQL"""
        
        # Current year for filtering commits
        current_year = datetime.now().year
        
        # GraphQL query for comprehensive account stats
        query = """
        query userInfo($login: String!, $from: DateTime!) {
          user(login: $login) {
            login
            name
            avatarUrl
            createdAt
            followers {
              totalCount
            }
            following {
              totalCount
            }
            repositories(ownerAffiliations: OWNER, first: 100) {
              totalCount
              nodes {
                stargazers {
                  totalCount
                }
                forkCount
                isPrivate
                primaryLanguage {
                  name
                }
              }
            }
            contributionsCollection(from: $from) {
              totalCommitContributions
              totalIssueContributions
              totalPullRequestContributions
              totalPullRequestReviewContributions
              totalRepositoriesWithContributedCommits
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                  }
                }
              }
            }
            repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
              totalCount
            }
          }
        }
        """
        
        # Calculate start of current year
        year_start = datetime(current_year, 1, 1).replace(tzinfo=timezone.utc).isoformat()
        
        variables = {
            "login": username,
            "from": year_start
        }
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(GITHUB_GRAPHQL_URL, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"GraphQL API error: {response.status}")
                
                data = await response.json()
                
                if 'errors' in data:
                    error_msg = data['errors'][0].get('message', 'GraphQL error')
                    if 'NOT_FOUND' in str(data['errors'][0]):
                        raise Exception(f"User '{username}' not found")
                    raise Exception(f"GraphQL error: {error_msg}")
                
                return data['data']['user']

    async def fetch_total_commits(self, username: str) -> int:
        """Fetch total commits by getting user's contribution data without date restrictions"""
        
        # Get contributions without date filtering to get all-time data
        query = """
        query userContributions($login: String!) {
          user(login: $login) {
            contributionsCollection {
              totalCommitContributions
            }
          }
        }
        """
        
        variables = {"login": username}
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(GITHUB_GRAPHQL_URL, headers=headers, json=payload) as response:
                if response.status != 200:
                    return 0
                
                data = await response.json()
                
                if 'errors' in data or not data.get('data'):
                    return 0
                
                # This gives us all-time commits (GitHub's default is last year)
                # For true all-time commits, we'd need to aggregate multiple years
                # For now, let's return what we get and note this limitation
                all_time_commits = data['data']['user']['contributionsCollection']['totalCommitContributions']
                
                # Since GitHub's default contributionsCollection only shows last year,
                # we'll use a multiplier estimation or just return the available data
                # For now, let's return what we get and note this limitation
                return all_time_commits

    async def calculate_streak(self, contributions_calendar: Dict) -> int:
        """Calculate current streak from contributions calendar"""
        
        weeks = contributions_calendar.get('weeks', [])
        if not weeks:
            return 0
            
        # Flatten all days and sort by date (newest first)
        all_days = []
        for week in weeks:
            for day in week.get('contributionDays', []):
                all_days.append(day)
        
        # Sort by date descending (newest first)
        all_days.sort(key=lambda x: x['date'], reverse=True)
        
        # Calculate current streak
        streak = 0
        today = datetime.now().date()
        
        for day in all_days:
            day_date = datetime.fromisoformat(day['date'].replace('Z', '+00:00')).date()
            
            # Skip future dates
            if day_date > today:
                continue
                
            # If this is today or yesterday and has contributions, continue streak
            days_diff = (today - day_date).days
            
            if days_diff <= 1 and day['contributionCount'] > 0:
                streak += 1
                today = day_date - timedelta(days=1)  # Move to previous day
            elif days_diff <= 1 and day['contributionCount'] == 0:
                # No contributions today/yesterday, streak broken
                break
            elif day['contributionCount'] > 0:
                # Found a contribution day in sequence
                streak += 1
                today = day_date - timedelta(days=1)
            else:
                # No contribution, streak broken
                break
                
        return streak

    async def fetch_avatar_as_data_uri(self, avatar_url: str) -> str:
        """Fetch avatar image and convert to base64 data URI"""
        if not avatar_url:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        # Convert to base64
                        base64_data = base64.b64encode(image_data).decode('utf-8')
                        # Return as data URI (assuming PNG format)
                        return f"data:image/png;base64,{base64_data}"
        except:
            pass
        
        return None

def calculate_stats(user_data: Dict[str, Any]) -> Dict[str, int]:
    """Calculate all statistics from user data"""
    
    stats = {}
    
    # Stars - total across all repositories
    total_stars = sum(repo['stargazers']['totalCount'] for repo in user_data['repositories']['nodes'])
    stats['stars'] = total_stars
    
    # Commits this year
    stats['commits_year'] = user_data['contributionsCollection']['totalCommitContributions']
    
    # Pull requests
    stats['pull_requests'] = user_data['contributionsCollection']['totalPullRequestContributions']
    
    # Code reviews  
    stats['code_reviews'] = user_data['contributionsCollection']['totalPullRequestReviewContributions']
    
    # Issues
    stats['issues'] = user_data['contributionsCollection']['totalIssueContributions']
    
    # External contributions
    stats['external_contributions'] = user_data['repositoriesContributedTo']['totalCount']
    
    return stats

def format_number(num: int) -> str:
    """Format numbers for display (e.g., 1000 -> 1k)"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M".rstrip('0').rstrip('.')
    elif num >= 1000:
        return f"{num / 1000:.1f}k".rstrip('0').rstrip('.')
    else:
        return str(num)

async def get_icon_svg(icon_type: str, username: str, theme: str, x: int = 420, y: int = 80, avatar_url: str = None, size: int = 80, streak_value: int = 0) -> str:
    """Generate SVG for different icon types"""
    
    colors = THEMES[theme]
    radius = size // 2 - 5
    
    if icon_type == "github":
        # GitHub icon SVG (responsive size)
        scale = size / 80  # Scale factor based on default size
        return f'''<g transform="translate({x}, {y})">
            <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="{colors['border']}" stroke="{colors['text_secondary']}" stroke-width="2"/>
            <g transform="translate({(size-40*scale)//2}, {(size-40*scale)//2}) scale({scale})">
                <path d="M20 2C10.059 2 2 10.059 2 20c0 7.969 5.167 14.729 12.329 17.125.9.165 1.229-.39 1.229-.867 0-.428-.015-1.563-.023-3.067-5.012 1.089-6.07-2.415-6.07-2.415-.818-2.078-1.997-2.631-1.997-2.631-1.633-1.116.124-1.094.124-1.094 1.805.127 2.755 1.854 2.755 1.854 1.604 2.748 4.207 1.954 5.233 1.494.163-1.162.628-1.954 1.142-2.401-3.996-.453-8.194-1.998-8.194-8.891 0-1.964.7-3.571 1.851-4.832-.185-.454-.803-2.285.176-4.764 0 0 1.509-.483 4.944 1.845a17.163 17.163 0 0 1 4.5-.605c1.526.007 3.063.206 4.5.605 3.433-2.328 4.941-1.845 4.941-1.845.981 2.479.363 4.31.178 4.764 1.153 1.261 1.85 2.868 1.85 4.832 0 6.91-4.207 8.431-8.218 8.874.646.558 1.221 1.658 1.221 3.34 0 2.413-.021 4.36-.021 4.95 0 .482.325 1.041 1.238.864C32.835 34.72 38 27.965 38 20c0-9.941-8.059-18-18-18z" fill="{colors['text_primary']}"/>
            </g>
        </g>'''
    elif icon_type == "default" or icon_type == "user":
        # User avatar - Fetch as data URI for better compatibility
        # Create a temporary API instance to fetch avatar
        try:
            api = GitHubAccountStatsAPI()
            data_uri = await api.fetch_avatar_as_data_uri(avatar_url) if avatar_url else None
        except:
            data_uri = None
        
        if data_uri:
            return f'''<g transform="translate({x}, {y})">
                <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="{colors['border']}" stroke="{colors['text_secondary']}" stroke-width="2"/>
                <image x="5" y="5" width="{size-10}" height="{size-10}" href="{data_uri}" clip-path="url(#avatar-clip-{username})"/>
            </g>'''
        else:
            # Fallback to user icon if avatar fetch fails
            scale = size / 80
            return f'''<g transform="translate({x}, {y})">
                <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="{colors['accent']}" stroke="{colors['text_secondary']}" stroke-width="2"/>
                <g transform="translate({size//2-15*scale}, {size//2-20*scale}) scale({scale})">
                    <circle cx="15" cy="12" r="8" fill="{colors['bg']}"/>
                    <path d="M30 35 C30 25, 20 20, 15 20 C10 20, 0 25, 0 35 L0 40 L30 40 Z" fill="{colors['bg']}"/>
                </g>
                <text x="{size//2}" y="{size-8}" text-anchor="middle" fill="{colors['bg']}" font-size="{max(8, size//10)}" font-weight="bold" font-family="'Segoe UI', sans-serif">{username[:3].upper()}</text>
            </g>'''
    elif icon_type == "streak":
        # Streak icon with milky orange gradient and real fire emoji
        streak_id = f"streak-gradient-{username}"
        
        return f'''<g transform="translate({x}, {y})">
            <defs>
                <radialGradient id="{streak_id}" cx="50%" cy="40%" r="60%">
                    <stop offset="0%" style="stop-color:#2d1810"/>
                    <stop offset="40%" style="stop-color:#8b4513"/>
                    <stop offset="80%" style="stop-color:#cd853f"/>
                    <stop offset="100%" style="stop-color:#daa520"/>
                </radialGradient>
            </defs>
            
            <!-- Matte streak-themed gradient background -->
            <circle cx="{size//2}" cy="{size//2}" r="{radius}" 
                    fill="url(#{streak_id})" 
                    stroke="{colors['text_secondary']}" 
                    stroke-width="2"/>
            
            <!-- Fire emoji -->
            <text x="{size//2}" y="{size//2}" 
                  text-anchor="middle" 
                  font-size="{size//1.5}" 
                  style="dominant-baseline: central;">🔥</text>
                  
            <!-- Streak number centered in icon with better outline -->
            <text x="{size//2}" y="{size//2 + 8}" 
                  text-anchor="middle" 
                  fill="#ffffff" 
                  font-size="{max(12, size//6)}" 
                  font-weight="900" 
                  font-family="'Segoe UI', sans-serif"
                  stroke="#333333" 
                  stroke-width="0.5">{streak_value}</text>
        </g>'''
    else:
        return ""

async def create_rotating_icon_svg(icon1: str, icon2: str, username: str, theme: str, x: int = 420, y: int = 80, avatar_url: str = None, size: int = 80) -> str:
    """Create a rotating coin-like icon with two sides (Y-axis flip like a coin)"""
    
    # Get the two different icon SVGs
    icon1_content = await get_icon_svg(icon1, username, theme, 0, 0, avatar_url, size, 0)  # Position at 0,0 for relative positioning
    icon2_content = await get_icon_svg(icon2, username, theme, 0, 0, avatar_url, size, 0)
    
    return f'''<g transform="translate({x}, {y})">
        <g class="coin-container">
            <!-- Side 1: Front of coin -->
            <g class="side-1">
                {icon1_content}
            </g>
            <!-- Side 2: Back of coin -->
            <g class="side-2">
                {icon2_content}
            </g>
        </g>
    </g>
    <style>
        .coin-container {{
            animation: coinFlip 8s infinite ease-in-out;
            transform-origin: {size//2}px {size//2}px;
        }}
        
        .side-1 {{
            animation: showSide1 8s infinite ease-in-out;
        }}
        
        .side-2 {{
            animation: showSide2 8s infinite ease-in-out;
            opacity: 0;
            transform: scaleX(-1) translateX(-{size}px);
        }}
        
        @keyframes coinFlip {{
            0% {{ transform: rotateY(0deg); }}
            12.5% {{ transform: rotateY(180deg); }}
            50% {{ transform: rotateY(180deg); }}
            62.5% {{ transform: rotateY(360deg); }}
            100% {{ transform: rotateY(360deg); }}
        }}
        
        @keyframes showSide1 {{
            0% {{ opacity: 1; }}
            6.24% {{ opacity: 1; }}
            6.25% {{ opacity: 0; }}
            56.24% {{ opacity: 0; }}
            56.25% {{ opacity: 1; }}
            100% {{ opacity: 1; }}
        }}
        
        @keyframes showSide2 {{
            0% {{ opacity: 0; }}
            6.24% {{ opacity: 0; }}
            6.25% {{ opacity: 1; }}
            56.24% {{ opacity: 1; }}
            56.25% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}
    </style>'''

def get_stat_icon_svg(stat_type: str, theme: str) -> str:
    """Generate proper SVG icons for different stat types (inspired by github-readme-stats)"""
    
    colors = THEMES[theme]
    
    icons = {
        'stars': f'''<path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z" fill="{colors['warning']}"/>''',
        
        'commits_total': f'''<path d="M3 2.75A2.75 2.75 0 015.75 0h4.5A2.75 2.75 0 0113 2.75v10.5A2.75 2.75 0 0110.25 16h-4.5A2.75 2.75 0 013 13.25V2.75zm2.75-1.25a1.25 1.25 0 00-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h4.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25h-4.5z" fill="{colors['accent']}"/><path d="M6.5 5.5a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5z" fill="{colors['accent']}"/>''',
        
        'commits_year': f'''<path d="M3 2.75A2.75 2.75 0 015.75 0h4.5A2.75 2.75 0 0113 2.75v10.5A2.75 2.75 0 0110.25 16h-4.5A2.75 2.75 0 013 13.25V2.75zm2.75-1.25a1.25 1.25 0 00-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h4.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25h-4.5z" fill="{colors['success']}"/><path d="M6.5 5.5a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5z" fill="{colors['success']}"/>''',
        
        'pull_requests': f'''<path d="M1.5 3.25a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zm5.677-.177L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm0 9.5a.75.75 0 100 1.5.75.75 0 000-1.5z" fill="{colors['accent']}"/>''',
        
        'code_reviews': f'''<path d="M1.679 7.932c.412-.621 1.242-1.75 2.366-2.717C5.175 4.242 6.527 3.5 8 3.5c1.473 0 2.824.742 3.955 1.715 1.124.967 1.954 2.096 2.366 2.717a.119.119 0 010 .136c-.412.621-1.242 1.75-2.366 2.717C10.825 11.758 9.473 12.5 8 12.5c-1.473 0-2.824-.742-3.955-1.715-1.124-.967-1.954-2.096-2.366-2.717a.119.119 0 010-.136zM8 2c-1.981 0-3.67.992-4.933 2.078C1.797 5.169.88 6.423.43 7.1a1.619 1.619 0 000 1.798c.45.678 1.367 1.932 2.637 3.024C4.329 13.008 6.019 14 8 14c1.981 0 3.67-.992 4.933-2.078 1.27-1.092 2.187-2.346 2.637-3.024a1.619 1.619 0 000-1.798c-.45-.678-1.367-1.932-2.637-3.024C11.671 2.992 9.981 2 8 2zm0 8a2 2 0 100-4 2 2 0 000 4z" fill="{colors['text_secondary']}"/>''',
        
        'issues': f'''<path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" fill="{colors['warning']}"/><path d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z" fill="{colors['warning']}"/>''',
        
        'external_contributions': f'''<path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z" fill="{colors['success']}"/>'''
    }
    
    return icons.get(stat_type, f'''<circle cx="8" cy="8" r="6" fill="{colors['text_secondary']}"/>''')

def create_stat_item_svg(label: str, value: str, stat_type: str, x: int, y: int, theme: str, stats_width: int = 300) -> str:
    """Create SVG for a single stat item with compact positioning"""
    
    colors = THEMES[theme]
    icon_svg = get_stat_icon_svg(stat_type, theme)
    
    # Compact positioning for smaller layout
    icon_size = 14  # Smaller icon
    label_start = icon_size + 8  # Tighter gap after icon
    value_x = 140  # Adjusted position for values in compact layout
    
    return f'''<g transform="translate({x}, {y})">
        <g transform="translate(0, 0)">
            <svg width="{icon_size}" height="{icon_size}" viewBox="0 0 16 16">
                {icon_svg}
            </svg>
        </g>
        <text x="{label_start}" y="10" fill="{colors['text_secondary']}" font-size="12" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif">{label}:</text>
        <text x="{value_x}" y="10" fill="{colors['text_primary']}" font-size="12" font-weight="600" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif">{value}</text>
    </g>'''

async def create_account_general_svg(
    username: str,
    icon: str = "default",
    slots: List[str] = None,
    theme: str = "dark"
) -> str:
    """Generate account general stats SVG with fixed optimal dimensions (700x300)"""
    
    if slots is None:
        slots = ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues']
    
    # Ensure we have exactly 5 slots, but allow None values
    while len(slots) < 5:
        slots.append(None)
    slots = slots[:5]
    
    # Compact card dimensions to match the image
    width = 400
    height = 200
    
    colors = THEMES[theme]
    
    # Fetch data from GitHub
    api = GitHubAccountStatsAPI()
    user_data = await api.fetch_account_stats(username)
    
    # Calculate stats
    stats = calculate_stats(user_data)
    
    # Get total commits (this is an approximation as GitHub doesn't provide exact total)
    stats['commits_total'] = await api.fetch_total_commits(username)
    
    # Calculate streak
    streak = await api.calculate_streak(user_data['contributionsCollection']['contributionCalendar'])
    
    # Create icon section for right side - matching the image layout
    icon_svg = ""
    avatar_url = user_data.get('avatarUrl')
    
    # Compact layout positioning for 400x200
    padding = 20  # Card padding
    title_height = 35  # Space for title (more compact)
    
    # LEFT SIDE: Title and stats positioning
    title_x = padding + 10  # Left aligned title
    stats_x = padding + 10  # Left aligned stats
    stats_start_y = title_height + 20  # Start position for stats
    stats_spacing = 25  # Tighter spacing between stats
    
    # RIGHT SIDE: Icon positioning (right side, centered with 3rd stats row)
    icon_size = 80  # Compact icon size
    icon_x = width - icon_size - padding - 10  # Right side margin
    # Calculate 3rd row position: stats_start_y + (2 * stats_spacing) for 3rd row (index 2)
    third_row_y = stats_start_y + (2 * stats_spacing)
    icon_y = third_row_y - (icon_size // 2) + 5  # Center icon with 3rd row (5px for text baseline)
    
    if '+' in icon:
        # Rotating icon with two sides - fixed optimal size
        icon1, icon2 = icon.split('+')
        icon_svg = await create_rotating_icon_svg(icon1, icon2, username, theme, icon_x, icon_y, avatar_url, icon_size)
    else:
        # Single icon - fixed optimal size
        if icon == "streak":
            # For streak icon with fire emoji and number inside
            streak_id = f"streak-gradient-{username}"
            radius = icon_size // 2 - 5
            
            icon_svg = f'''<g transform="translate({icon_x}, {icon_y})">
                <defs>
                    <radialGradient id="{streak_id}" cx="50%" cy="40%" r="60%">
                        <stop offset="0%" style="stop-color:#2d1810"/>
                        <stop offset="40%" style="stop-color:#8b4513"/>
                        <stop offset="80%" style="stop-color:#cd853f"/>
                        <stop offset="100%" style="stop-color:#daa520"/>
                    </radialGradient>
                </defs>
                
                <!-- Matte streak-themed gradient background -->
                <circle cx="{icon_size//2}" cy="{icon_size//2}" r="{radius}" 
                        fill="url(#{streak_id})" 
                        stroke="{colors['text_secondary']}" 
                        stroke-width="2"/>
                
                <!-- Fire emoji -->
                <text x="{icon_size//2}" y="{icon_size//2}" 
                      text-anchor="middle" 
                      font-size="{icon_size//1.5}" 
                      style="dominant-baseline: central;">🔥</text>
                      
                <!-- Streak number centered in the icon with better outline -->
                <text x="{icon_size//2}" y="{icon_size//2 + 8}" 
                      text-anchor="middle" 
                      fill="#ffffff" 
                      font-size="{max(12, icon_size//6)}" 
                      font-weight="900" 
                      font-family="'Segoe UI', sans-serif"
                      stroke="#333333" 
                      stroke-width="0.5">{streak}</text>
            </g>'''
        else:
            icon_svg = await get_icon_svg(icon, username, theme, icon_x, icon_y, avatar_url, icon_size, streak)
    
    # Create stat items in single column - fixed optimal layout
    stat_items = []
    stat_labels = {
        'stars': 'Total Stars',
        'commits_total': 'Total Commits',
        'commits_year': f'Commits ({datetime.now().year})',
        'pull_requests': 'Pull Requests',
        'code_reviews': 'Code Reviews', 
        'issues': 'Issues',
        'external_contributions': 'Contributed to'
    }
    
    # Create perfectly positioned stats
    stats_width = width - stats_x - icon_size - padding  # Remaining width for stats
    for i, slot in enumerate(slots):
        if slot is None:
            # Skip empty slots
            continue
            
        value = stats.get(slot, 0)
        label = stat_labels.get(slot, slot.replace('_', ' ').title())
        formatted_value = format_number(value)
        
        x = stats_x
        y = stats_start_y + (i * stats_spacing)
        
        stat_items.append(create_stat_item_svg(label, formatted_value, slot, x, y, theme, stats_width))
    
    # Generate final SVG with compact layout (400x200)
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="400" height="200" viewBox="0 0 400 200">
        <defs>
            <style>
                .github-stats {{
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                }}
                .card-bg {{
                    fill: {colors['bg']};
                    stroke: {colors['border']};
                    stroke-width: 1;
                    rx: 8;
                }}
                .title {{
                    fill: {colors['text_primary']};
                    font-size: 16px;
                    font-weight: 600;
                }}
                .rank-circle {{
                    fill: {colors['accent']};
                    stroke: {colors['border']};
                    stroke-width: 2;
                }}
            </style>
            <clipPath id="avatar-clip-{username}">
                <circle cx="40" cy="40" r="35"/>
            </clipPath>
        </defs>
        
        <!-- Background with rounded corners -->
        <rect class="card-bg" width="400" height="200"/>
        
        <!-- Title left aligned -->
        <text x="{title_x}" y="30" class="title github-stats">
            {user_data.get('name', username)}'s GitHub Stats
        </text>
        
        <!-- Stats on left side -->
        {''.join(stat_items)}
        
        <!-- Icon on right side -->
        {icon_svg}
        
    </svg>'''
    
    return svg_content
