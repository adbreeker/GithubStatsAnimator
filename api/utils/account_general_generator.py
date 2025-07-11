"""
GitHub Account General Stats SVG Generator
Creates an SVG representation of GitHub account general statistics using GraphQL API.

This module provides functionality to:
- Fetch comprehensive GitHub statistics via GraphQL
- Generate customizable SVG cards with user stats
- Support various themes and icon types
- Optimize API calls based on required statistics
"""

import asyncio
import aiohttp
import base64
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Theme configurations for light and dark modes
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

# Stat type configurations with labels and descriptions
STAT_CONFIGS = {
    'commits_6_months': {
        'label': 'Commits (6 months)',
        'description': 'Commits in the last 6 months',
        'expensive': False
    },
    'stars': {
        'label': 'Total Stars',
        'description': 'Total stars across all repositories',
        'expensive': False
    },
    'commits_total': {
        'label': 'Total Commits',
        'description': 'All-time commits (requires year-by-year API calls)',
        'expensive': True
    },
    'commits_current_year': {
        'label': f'Commits ({datetime.now().year})',
        'description': 'Commits in current year',
        'expensive': False
    },
    'pull_requests': {
        'label': 'Pull Requests',
        'description': 'Total pull requests created',
        'expensive': False
    },
    'code_reviews': {
        'label': 'Code Reviews',
        'description': 'All-time pull request reviews (requires year-by-year API calls)',
        'expensive': True
    },
    'issues': {
        'label': 'Issues',
        'description': 'Total issues created',
        'expensive': False
    },
    'external_contributions': {
        'label': 'Contributed to',
        'description': 'Repositories contributed to',
        'expensive': False
    },
    'streak': {
        'label': 'Current Streak',
        'description': 'Current contribution streak (requires calendar processing)',
        'expensive': True
    }
}

class GitHubAccountStatsAPI:
    """
    GitHub API client for fetching comprehensive account statistics.
    
    Provides methods to fetch user data efficiently, with optimization for
    expensive operations like all-time commits and code reviews.
    """
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    async def _make_graphql_request(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make a GraphQL request to GitHub API with error handling."""
        payload = {"query": query, "variables": variables}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(GITHUB_GRAPHQL_URL, headers=self.headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"GraphQL API error: {response.status}")
                
                data = await response.json()
                
                if 'errors' in data:
                    error_msg = data['errors'][0].get('message', 'GraphQL error')
                    if 'NOT_FOUND' in str(data['errors'][0]):
                        raise Exception(f"User not found")
                    raise Exception(f"GraphQL error: {error_msg}")
                
                return data['data']

    async def fetch_avatar_as_data_uri(self, avatar_url: str) -> Optional[str]:
        """Fetch avatar image and convert to base64 data URI for embedding."""
        if not avatar_url:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        base64_data = base64.b64encode(image_data).decode('utf-8')
                        return f"data:image/png;base64,{base64_data}"
        except Exception:
            pass
        
        return None

    async def fetch_account_stats(self, username: str, needed_stats: set = None) -> Dict[str, Any]:
        """
        Fetch comprehensive account statistics using exactly TWO GraphQL queries:
        1. Basic user data (user, repos, PRs, issues, repositories contributed to)
        2. All-time data (commits, code reviews, contribution calendar for streak)
        """
        if needed_stats is None:
            needed_stats = set()
        
        # FIRST QUERY: Basic user information
        basic_query = """
        query userBasicInfo($login: String!) {
          user(login: $login) {
            login
            name
            avatarUrl
            createdAt
            followers { totalCount }
            following { totalCount }
            repositories(ownerAffiliations: OWNER, first: 100) {
              totalCount
              nodes {
                stargazers { totalCount }
                forkCount
                isPrivate
                primaryLanguage { name }
              }
            }
            repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
              totalCount
            }
            pullRequests(first: 1) { totalCount }
            issues(first: 1) { totalCount }
          }
        }
        """
        
        # Execute first query
        basic_data = await self._make_graphql_request(basic_query, {"login": username})
        user_data = basic_data['user']
        
        # Extract creation date for second query
        created_at = user_data['createdAt']
        creation_date = created_at.split('T')[0] + 'T00:00:00Z'  # Account creation date
        
        # Get current date and year ranges for second query
        today = datetime.now().replace(tzinfo=timezone.utc)
        current_date = today.isoformat()
        
        # Current year start for commits_year stat
        current_year = datetime.now().year
        current_year_start = datetime(current_year, 1, 1).replace(tzinfo=timezone.utc).isoformat()
        
        # For contribution calendar (one year ago to today)
        one_year_ago = today - timedelta(days=365)
        year_start = one_year_ago.isoformat()
        
        # Build second query parts based on needed stats
        second_query_parts = []
        
        # Always include current year commits if commits_current_year is needed
        if 'commits_current_year' in needed_stats:
            second_query_parts.append(f"""currentYearCommits: contributionsCollection(from: "{current_year_start}") {{
              totalCommitContributions
            }}""")
        # Add last 6 months commits if needed
        if 'commits_6_months' in needed_stats:
            six_months_ago = (today - timedelta(days=183)).isoformat()
            second_query_parts.append(f"""last6MonthsCommits: contributionsCollection(from: "{six_months_ago}") {{
              totalCommitContributions
            }}""")
        
        # Add all-time data if needed (year by year chunks)
        if 'commits_total' in needed_stats or 'code_reviews' in needed_stats:
            # Extract creation year from creation date
            creation_year = int(created_at[:4])
            current_year = datetime.now().year
            
            # Build year-by-year queries for all-time data
            for year in range(creation_year, current_year + 1):
                year_from = f"{year}-01-01T00:00:00Z"
                year_to = f"{year}-12-31T23:59:59Z"
                
                year_parts = []
                if 'commits_total' in needed_stats:
                    year_parts.append("totalCommitContributions")
                if 'code_reviews' in needed_stats:
                    year_parts.append("totalPullRequestReviewContributions")
                
                second_query_parts.append(f"""year{year}Data: contributionsCollection(from: "{year_from}", to: "{year_to}") {{
                  {chr(10).join(['                  ' + part for part in year_parts])}
                }}""")
        
        # Add contribution calendar for streak if needed
        if 'streak' in needed_stats:
            second_query_parts.append(f"""contributionCalendar: contributionsCollection(from: "{year_start}") {{
              contributionCalendar {{
                totalContributions
                weeks {{
                  contributionDays {{
                    contributionCount
                    date
                  }}
                }}
              }}
            }}""")
        
        # SECOND QUERY: All-time and current year data (only if needed)
        if second_query_parts:
            alltime_query = f"""
            query userAllTimeData($login: String!) {{
              user(login: $login) {{
                {chr(10).join(['                ' + part for part in second_query_parts])}
              }}
            }}
            """
            
            # Execute second query
            alltime_data = await self._make_graphql_request(alltime_query, {"login": username})
            alltime_user = alltime_data['user']
            
            # Add current year commits to user_data
            if 'commits_current_year' in needed_stats and 'currentYearCommits' in alltime_user:
                user_data['currentYearCommits'] = alltime_user['currentYearCommits']['totalCommitContributions']
            # Add last 6 months commits to user_data
            if 'commits_6_months' in needed_stats and 'last6MonthsCommits' in alltime_user:
                user_data['last6MonthsCommits'] = alltime_user['last6MonthsCommits']['totalCommitContributions']
            
            # Process year-by-year all-time data
            if 'commits_total' in needed_stats or 'code_reviews' in needed_stats:
                creation_year = int(user_data['createdAt'][:4])
                current_year = datetime.now().year
                
                if 'commits_total' in needed_stats:
                    total_commits = 0
                    for year in range(creation_year, current_year + 1):
                        year_key = f'year{year}Data'
                        if year_key in alltime_user and 'totalCommitContributions' in alltime_user[year_key]:
                            total_commits += alltime_user[year_key]['totalCommitContributions']
                    user_data['totalCommits'] = total_commits
                
                if 'code_reviews' in needed_stats:
                    total_reviews = 0
                    for year in range(creation_year, current_year + 1):
                        year_key = f'year{year}Data'
                        if year_key in alltime_user and 'totalPullRequestReviewContributions' in alltime_user[year_key]:
                            total_reviews += alltime_user[year_key]['totalPullRequestReviewContributions']
                    user_data['totalCodeReviews'] = total_reviews
            
            # Add streak data
            if 'streak' in needed_stats and 'contributionCalendar' in alltime_user:
                user_data['contributionCalendar'] = alltime_user['contributionCalendar']['contributionCalendar']
                user_data['currentStreak'] = await calculate_streak(user_data['contributionCalendar'])
        
        return user_data

def calculate_basic_stats(user_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate all statistics from consolidated user data.
    
    Now using data from the two-query approach:
    - Basic stats from first query
    - All-time stats from second query (if available)
    """
    stats = {}
    
    # Total stars across all repositories
    total_stars = sum(repo['stargazers']['totalCount'] 
                     for repo in user_data['repositories']['nodes'])
    stats['stars'] = total_stars
    
    # Total commits (if available from second query)
    if 'totalCommits' in user_data:
        stats['commits_total'] = user_data['totalCommits']
    
    # Total code reviews (if available from second query)
    if 'totalCodeReviews' in user_data:
        stats['code_reviews'] = user_data['totalCodeReviews']
    
    # Current year commits (if available from second query)
    if 'currentYearCommits' in user_data:
        stats['commits_current_year'] = user_data['currentYearCommits']
    else:
        stats['commits_current_year'] = 0

    if 'last6MonthsCommits' in user_data:
        stats['commits_6_months'] = user_data['last6MonthsCommits']
    else:
        stats['commits_6_months'] = 0
    
    # Pull requests (use all-time data from pullRequests field)
    stats['pull_requests'] = user_data.get('pullRequests', {}).get('totalCount', 0)
    
    # Issues (use all-time data from issues field)
    stats['issues'] = user_data.get('issues', {}).get('totalCount', 0)
    
    # External contributions (repositories contributed to)
    stats['external_contributions'] = user_data['repositoriesContributedTo']['totalCount']
    
    # Current streak (if available from second query)
    if 'currentStreak' in user_data:
        stats['streak'] = user_data['currentStreak']
    
    return stats


async def calculate_streak(contributions_calendar: Dict) -> int:
    """
    Calculate current contribution streak from calendar data.

    Start from yesterday and count backwards, then add 1 if today has contributions.
    This approach is more accurate as it doesn't include today's incomplete day in the base streak.
    """
    weeks = contributions_calendar.get('weeks', [])
    if not weeks:
        return 0
    
    # Flatten all days and sort by date (newest first)
    all_days = []
    for week in weeks:
        for day in week.get('contributionDays', []):
            all_days.append(day)
    
    all_days.sort(key=lambda x: x['date'], reverse=True)
    
    today = datetime.now().date()
    
    # Start streak calculation from yesterday, going backwards
    streak = 0
    
    for day in all_days:
        day_date = datetime.fromisoformat(day['date'].replace('Z', '+00:00')).date()
        
        if day_date == today:
            # If today has contributions, count it as part of the streak
            if day['contributionCount'] > 0:
                streak += 1
        else:
            # If we hit a day without contributions, stop counting
            if day['contributionCount'] == 0:
                break
            streak += 1
    return streak       

def format_number(num: int) -> str:
    """Format numbers for display (e.g., 1000 -> 1k, 1500000 -> 1.5M)."""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M".rstrip('0').rstrip('.')
    elif num >= 1000:
        return f"{num / 1000:.1f}k".rstrip('0').rstrip('.')
    else:
        return str(num)

async def generate_icon_svg(icon_type: str, username: str, theme: str, x: int, y: int, 
                           avatar_url: str = None, size: int = 80, streak_value: int = 0) -> str:
    """
    Generate SVG for different icon types including user avatar, GitHub logo, and streak.
    
    Supports various icon types with consistent sizing and positioning.
    """
    colors = THEMES[theme]
    radius = size // 2 - 5
    
    if icon_type == "github":
        # GitHub logo icon
        scale = size / 80
        return f'''<g transform="translate({x}, {y})">
            <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="{colors['border']}" stroke="{colors['text_secondary']}" stroke-width="2"/>
            <g transform="translate({(size-40*scale)//2}, {(size-40*scale)//2}) scale({scale})">
                <path d="M20 2C10.059 2 2 10.059 2 20c0 7.969 5.167 14.729 12.329 17.125.9.165 1.229-.39 1.229-.867 0-.428-.015-1.563-.023-3.067-5.012 1.089-6.07-2.415-6.07-2.415-.818-2.078-1.997-2.631-1.997-2.631-1.633-1.116.124-1.094.124-1.094 1.805.127 2.755 1.854 2.755 1.854 1.604 2.748 4.207 1.954 5.233 1.494.163-1.162.628-1.954 1.142-2.401-3.996-.453-8.194-1.998-8.194-8.891 0-1.964.7-3.571 1.851-4.832-.185-.454-.803-2.285.176-4.764 0 0 1.509-.483 4.944 1.845a17.163 17.163 0 0 1 4.5-.605c1.526.007 3.063.206 4.5.605 3.433-2.328 4.941-1.845 4.941-1.845.981 2.479.363 4.31.178 4.764 1.153 1.261 1.85 2.868 1.85 4.832 0 6.91-4.207 8.431-8.218 8.874.646.558 1.221 1.658 1.221 3.34 0 2.413-.021 4.36-.021 4.95 0 .482.325 1.041 1.238.864C32.835 34.72 38 27.965 38 20c0-9.941-8.059-18-18-18z" fill="{colors['text_primary']}"/>
            </g>
        </g>'''
    
    elif icon_type == "user":
        # User avatar with fallback
        api = GitHubAccountStatsAPI()
        try:
            data_uri = await api.fetch_avatar_as_data_uri(avatar_url) if avatar_url else None
        except Exception:
            data_uri = None
        
        if data_uri:
            return f'''<g transform="translate({x}, {y})">
                <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="{colors['border']}" stroke="{colors['text_secondary']}" stroke-width="2"/>
                <image x="5" y="5" width="{size-10}" height="{size-10}" href="{data_uri}" clip-path="url(#avatar-clip-{username})"/>
            </g>'''
        else:
            # Fallback to user icon with initials
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
        # Streak icon with fire emoji and streak number
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
            <circle cx="{size//2}" cy="{size//2}" r="{radius}" 
                    fill="url(#{streak_id})" 
                    stroke="{colors['text_secondary']}" 
                    stroke-width="2"/>
            <text x="{size//2}" y="{size//2}" 
                  text-anchor="middle" 
                  font-size="{size//1.5}" 
                  style="dominant-baseline: central;">🔥</text>
            <text x="{size//2}" y="{size//2 + 8}" 
                  text-anchor="middle" 
                  fill="#ffffff" 
                  font-size="{max(12, size//6)}" 
                  font-weight="900" 
                  font-family="'Segoe UI', sans-serif"
                  stroke="#333333" 
                  stroke-width="0.5">{streak_value}</text>
        </g>'''
    
    return ""  # Unknown icon type


async def create_rotating_icon_svg(icon1: str, icon2: str, username: str, theme: str, 
                                 x: int, y: int, avatar_url: str = None, size: int = 80, 
                                 streak_value: int = 0, animation_time: float = 8) -> str:
    """Create a rotating coin-like icon with two sides (Y-axis flip animation)."""
    # Generate both icon sides with proper streak value
    icon1_content = await generate_icon_svg(icon1, username, theme, 0, 0, avatar_url, size, streak_value)
    icon2_content = await generate_icon_svg(icon2, username, theme, 0, 0, avatar_url, size, streak_value)
    
    return f'''<g transform="translate({x}, {y})">
        <g class="coin-container">
            <g class="side-1">{icon1_content}</g>
            <g class="side-2">{icon2_content}</g>
        </g>
    </g>
    <style>
        .coin-container {{
            animation: coinFlip {animation_time}s infinite ease-in-out;
            transform-origin: {size//2}px {size//2}px;
        }}
        .side-1 {{ animation: showSide1 {animation_time}s infinite ease-in-out; }}
        .side-2 {{ 
            animation: showSide2 {animation_time}s infinite ease-in-out;
            opacity: 0;
            transform: scaleX(-1) translateX(-{size}px);
        }}
        @keyframes coinFlip {{
            0% {{ transform: rotateY(0deg); }}
            45.45% {{ transform: rotateY(0deg); }}
            50% {{ transform: rotateY(180deg); }}
            95.45% {{ transform: rotateY(180deg); }}
            100% {{ transform: rotateY(360deg); }}
        }}
        @keyframes showSide1 {{
            0%, 47.72%, 97.73%, 100% {{ opacity: 1; }}
            47.73%, 97.72% {{ opacity: 0; }}
        }}
        @keyframes showSide2 {{
            0%, 47.72%, 97.73%, 100% {{ opacity: 0; }}
            47.73%, 97.72% {{ opacity: 1; }}
        }}
        }}
    </style>'''

def get_stat_icon_svg(stat_type: str, theme: str) -> str:
    """Generate SVG icons for different stat types (GitHub-style icons)."""
    colors = THEMES[theme]
    
    icon_paths = {
        'stars': f'<path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z" fill="{colors["warning"]}"/>',
        
        'commits_total': f'<path d="M3 2.75A2.75 2.75 0 015.75 0h4.5A2.75 2.75 0 0113 2.75v10.5A2.75 2.75 0 0110.25 16h-4.5A2.75 2.75 0 013 13.25V2.75zm2.75-1.25a1.25 1.25 0 00-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h4.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25h-4.5z" fill="{colors["accent"]}"/><path d="M6.5 5.5a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5z" fill="{colors["accent"]}"/>',
        
        'commits_current_year': f'<path d="M3 2.75A2.75 2.75 0 015.75 0h4.5A2.75 2.75 0 0113 2.75v10.5A2.75 2.75 0 0110.25 16h-4.5A2.75 2.75 0 013 13.25V2.75zm2.75-1.25a1.25 1.25 0 00-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h4.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25h-4.5z" fill="{colors["success"]}"/><path d="M6.5 5.5a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5z" fill="{colors["success"]}"/>',

        'commits_6_months': f'<path d="M3 2.75A2.75 2.75 0 015.75 0h4.5A2.75 2.75 0 0113 2.75v10.5A2.75 2.75 0 0110.25 16h-4.5A2.75 2.75 0 013 13.25V2.75zm2.75-1.25a1.25 1.25 0 00-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h4.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25h-4.5z" fill="{colors["success"]}"/><path d="M6.5 5.5a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5zm0 2a.5.5 0 01.5-.5h2a.5.5 0 010 1H7a.5.5 0 01-.5-.5z" fill="{colors["success"]}"/>',
        
        'pull_requests': f'<path d="M1.5 3.25a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zm5.677-.177L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm0 9.5a.75.75 0 100 1.5.75.75 0 000-1.5z" fill="{colors["accent"]}"/>',
        
        'code_reviews': f'<path d="M1.679 7.932c.412-.621 1.242-1.75 2.366-2.717C5.175 4.242 6.527 3.5 8 3.5c1.473 0 2.824.742 3.955 1.715 1.124.967 1.954 2.096 2.366 2.717a.119.119 0 010 .136c-.412.621-1.242 1.75-2.366 2.717C10.825 11.758 9.473 12.5 8 12.5c-1.473 0-2.824-.742-3.955-1.715-1.124-.967-1.954-2.096-2.366-2.717a.119.119 0 010-.136zM8 2c-1.981 0-3.67.992-4.933 2.078C1.797 5.169.88 6.423.43 7.1a1.619 1.619 0 000 1.798c.45.678 1.367 1.932 2.637 3.024C4.329 13.008 6.019 14 8 14c1.981 0 3.67-.992 4.933-2.078 1.27-1.092 2.187-2.346 2.637-3.024a1.619 1.619 0 000-1.798c-.45-.678-1.367-1.932-2.637-3.024C11.671 2.992 9.981 2 8 2zm0 8a2 2 0 100-4 2 2 0 000 4z" fill="{colors["text_secondary"]}"/>',
        
        'issues': f'<path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" fill="{colors["warning"]}"/><path d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z" fill="{colors["warning"]}"/>',
        
        'external_contributions': f'<path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z" fill="{colors["success"]}"/>'
    }
    
    return icon_paths.get(stat_type, f'<circle cx="8" cy="8" r="6" fill="{colors["text_secondary"]}"/>')


def create_stat_item_svg(label: str, value: str, stat_type: str, x: int, y: int, 
                        theme: str, stats_width: int = 300) -> str:
    """Create SVG for a single stat item with icon, label, and value."""
    colors = THEMES[theme]
    icon_svg = get_stat_icon_svg(stat_type, theme)
    
    # Layout positioning
    icon_size = 14
    label_start = icon_size + 8
    value_x = 150
    
    return f'''<g transform="translate({x}, {y})">
        <g transform="translate(0, 0)">
            <svg width="{icon_size}" height="{icon_size}" viewBox="0 0 16 16">
                {icon_svg}
            </svg>
        </g>
        <text x="{label_start}" y="10" fill="{colors['text_secondary']}" font-size="12" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif">{label}:</text>
        <text x="{value_x}" y="10" fill="{colors['text_primary']}" font-size="12" font-weight="600" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif">{value}</text>
    </g>'''

def create_account_general_svg(
    username: str,
    user_data: Dict[str, Any],
    icon_svg: str,
    stat_items: List[str],
    title_x: int,
    colors: Dict[str, str] = THEMES['dark'],
):
    # Generate final SVG
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="400" height="200" viewBox="0 0 400 200">
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
            </style>
            <clipPath id="avatar-clip-{username}">
                <circle cx="40" cy="40" r="35"/>
            </clipPath>
        </defs>
        
        <!-- Background with rounded corners -->
        <rect class="card-bg" width="400" height="200"/>
        
        <!-- Title -->
        <text x="{title_x}" y="30" class="title github-stats">
            {user_data.get('name', username)}'s GitHub Stats
        </text>
        
        <!-- Stats -->
        {''.join(stat_items)}
        
        <!-- Icon -->
        {icon_svg}
    </svg>'''

async def generate_account_general_svg(
    username: str,
    icon: str = "user",
    slots: List[str] = None,
    theme: str = "dark",
    animation_time: float = 8
) -> str:
    """
    Generate account general stats SVG with optimized single-query performance.
    
    Args:
        username: GitHub username
        icon: Icon type ('user', 'github', 'streak', 'user+github', etc.)
        slots: List of stats to display (max 5)
        theme: Theme ('dark' or 'light')
        animation_duration: Duration of icon animation in seconds (default: 8)
    
    Returns:
        SVG string with user stats and icon
    """
    # Set default slots if none provided
    if slots is None:
        slots = ['stars', 'commits_total', 'commits_current_year', 'pull_requests', 'issues']
    
    # Ensure exactly 5 slots, padding with None if needed
    while len(slots) < 5:
        slots.append(None)
    slots = slots[:5]
    
    # Fixed card dimensions for consistent layout
    width, height = 400, 200
    colors = THEMES[theme]
    
    # Determine which stats are needed
    needed_stats = {slot for slot in slots if slot is not None}
    
    # Check if streak is needed for icon display
    if 'streak' in icon or '+streak' in icon:
        needed_stats.add('streak')
    
    # Initialize API and fetch ALL data in one consolidated query
    api = GitHubAccountStatsAPI()
    user_data = await api.fetch_account_stats(username, needed_stats)
    
    # Calculate all stats from the consolidated data
    stats = calculate_basic_stats(user_data)
    
    # Layout positioning
    padding = 20
    title_height = 35
    title_x = padding + 10
    stats_x = padding + 10
    stats_start_y = title_height + 20
    stats_spacing = 25
    
    # Icon positioning (right side, aligned with 3rd row)
    icon_size = 80
    icon_x = width - icon_size - padding - 10
    third_row_y = stats_start_y + (2 * stats_spacing)
    icon_y = third_row_y - (icon_size // 2) + 5
    
    # Generate icon SVG
    avatar_url = user_data.get('avatarUrl')
    streak_value = stats.get('streak', 0)
    
    if '+' in icon:
        # Rotating icon
        icon1, icon2 = icon.split('+')
        icon_svg = await create_rotating_icon_svg(
            icon1, icon2, username, theme, icon_x, icon_y, avatar_url, icon_size, streak_value, animation_time)
    else:
        # Single icon
        icon_svg = await generate_icon_svg(
            icon, username, theme, icon_x, icon_y, avatar_url, icon_size, streak_value)
    
    # Create stat items
    stat_items = []
    stats_width = width - stats_x - icon_size - padding
    
    for i, slot in enumerate(slots):
        if slot is None:
            continue
        
        value = stats.get(slot, 0)
        label = STAT_CONFIGS.get(slot, {}).get('label', slot.replace('_', ' ').title())
        formatted_value = format_number(value)
        
        x = stats_x
        y = stats_start_y + (i * stats_spacing)
        
        stat_items.append(create_stat_item_svg(label, formatted_value, slot, x, y, theme, stats_width))
    
    return create_account_general_svg(username, user_data, icon_svg, stat_items, title_x, colors)
