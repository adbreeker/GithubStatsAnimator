"""
GitHub Top Languages SVG Generator - GraphQL Implementation
Creates an SVG representation of GitHub top languages with percentages
Uses GraphQL for much faster data fetching compared to REST API
"""
import aiohttp
import asyncio
import math
import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub GraphQL API endpoint
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Language colors (GitHub's official colors)
LANGUAGE_COLORS = {
    "JavaScript": "#f1e05a",
    "Python": "#3572a5",
    "Java": "#b07219",
    "TypeScript": "#2b7489",
    "C#": "#239120",
    "C++": "#f34b7d",
    "C": "#555555",
    "PHP": "#4f5d95",
    "Ruby": "#701516",
    "Go": "#00add8",
    "Rust": "#dea584",
    "Swift": "#ffac45",
    "Kotlin": "#f18e33",
    "HTML": "#e34c26",
    "CSS": "#1572b6",
    "Shell": "#89e051",
    "Dart": "#00b4ab",
    "R": "#198ce7",
    "Scala": "#c22d40",
    "Perl": "#0298c3",
    "Haskell": "#5e5086",
    "Lua": "#000080",
    "MATLAB": "#e16737",
    "Objective-C": "#438eff",
    "Vue": "#2c3e50",
    "Jupyter Notebook": "#da5b0b",
    "Dockerfile": "#384d54",
    "Makefile": "#427819",
    "TeX": "#3d6117",
    "YAML": "#cb171e",
    "JSON": "#292929",
}

# Default color for unknown languages
DEFAULT_LANGUAGE_COLOR = "#858585"

# SVG Themes
THEMES = {
    "light": {
        "bg_color": "#ffffff",
        "border_color": "#e1e4e8",
        "text_color": "#24292e",
        "title_color": "#24292e",
        "subtitle_color": "#586069"
    },
    "dark": {
        "bg_color": "#0d1117",
        "border_color": "#30363d",
        "text_color": "#e6edf3",
        "title_color": "#e6edf3", 
        "subtitle_color": "#7d8590"
    }
}

class GitHubLanguagesGraphQL:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("No GitHub token found in environment variables")
    
    async def fetch_top_languages_graphql(self, username: str, exclude_repos: List[str] = None) -> Dict:
        """Fetch top languages using GraphQL - much faster than REST API"""
        if exclude_repos is None:
            exclude_repos = []
            
        # GraphQL query based on github-readme-stats implementation
        query = """
        query userInfo($login: String!) {
          user(login: $login) {
            repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
              nodes {
                name
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    size
                    node {
                      color
                      name
                    }
                  }
                }
              }
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
                    raise Exception(f"GraphQL API error: {response.status}")
                
                data = await response.json()
                
                if 'errors' in data:
                    error_msg = data['errors'][0].get('message', 'GraphQL error')
                    if 'NOT_FOUND' in str(data['errors'][0]):
                        raise Exception(f"User '{username}' not found")
                    raise Exception(f"GraphQL error: {error_msg}")
                
                return data['data']['user']['repositories']['nodes']

async def get_top_languages_graphql(username: str, languages_count: int = 5, exclude_languages: List[str] = None, count_other_languages: bool = False, exclude_repos: List[str] = None) -> List[Tuple[str, float]]:
    """Get top languages using GraphQL - much faster implementation"""
    if exclude_repos is None:
        exclude_repos = []
    if exclude_languages is None:
        exclude_languages = []
        
    api = GitHubLanguagesGraphQL()
    
    # Get all repositories with languages in a single GraphQL query
    repos = await api.fetch_top_languages_graphql(username, exclude_repos)
    
    # Filter out excluded repositories
    exclude_set = set(exclude_repos)
    filtered_repos = [repo for repo in repos if repo['name'] not in exclude_set]
    
    # Aggregate language data
    language_bytes = {}
    exclude_languages_set = set(exclude_languages)
    
    for repo in filtered_repos:
        for language_edge in repo['languages']['edges']:
            language_name = language_edge['node']['name']
            
            # Skip excluded languages
            if language_name in exclude_languages_set:
                continue
                
            language_size = language_edge['size']
            
            if language_name in language_bytes:
                language_bytes[language_name] += language_size
            else:
                language_bytes[language_name] = language_size
    
    # Calculate percentages
    total_bytes = sum(language_bytes.values())
    if total_bytes == 0:
        return []
    
    # Sort by bytes and get top languages
    sorted_languages = sorted(language_bytes.items(), key=lambda x: x[1], reverse=True)
    top_languages = []
    
    # Handle "Other" category logic
    if count_other_languages and len(sorted_languages) > languages_count:
        # Get top N languages
        top_n_languages = sorted_languages[:languages_count]
        remaining_languages = sorted_languages[languages_count:]
        
        # Calculate percentages for top languages
        top_bytes = sum(bytes_count for _, bytes_count in top_n_languages)
        other_bytes = sum(bytes_count for _, bytes_count in remaining_languages)
        
        # Add top languages with their actual percentages
        for language, bytes_count in top_n_languages:
            percentage = (bytes_count / total_bytes) * 100
            top_languages.append((language, percentage))
        
        # Add "Other" category if there are remaining languages
        if other_bytes > 0:
            other_percentage = (other_bytes / total_bytes) * 100
            top_languages.append(("Other", other_percentage))
    else:
        # Original behavior: redistribute 100% among top languages only
        selected_languages = sorted_languages[:languages_count]
        selected_total_bytes = sum(bytes_count for _, bytes_count in selected_languages)
        
        if selected_total_bytes > 0:
            for language, bytes_count in selected_languages:
                # Redistribute percentages to sum to 100%
                percentage = (bytes_count / selected_total_bytes) * 100
                top_languages.append((language, percentage))
    
    return top_languages

def create_language_bar_chart(languages: List[Tuple[str, float]], theme: str, width: int, height: int, decimal_places: int) -> str:
    """Create SVG bar chart for languages"""
    colors = THEMES[theme]
    title = "Most Used Languages"
    
    # Calculate dimensions
    padding = 40
    title_height = 40
    chart_width = width - (2 * padding)
    chart_height = height - (2 * padding) - title_height
    bar_height = max(20, chart_height // len(languages) - 10) if languages else 20
    
    # Start SVG
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{width}" height="{height}" fill="{colors['bg_color']}" stroke="{colors['border_color']}" rx="10"/>
    
    <!-- Title -->
    <text x="{width/2}" y="30" text-anchor="middle" fill="{colors['title_color']}" 
          font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
          font-size="16" font-weight="600">{title}</text>
    '''
    
    if not languages:
        svg += f'''
    <text x="{width/2}" y="{height/2}" text-anchor="middle" fill="{colors['subtitle_color']}" 
          font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
          font-size="14">No language data available</text>
    '''
    else:
        # Add language bars
        y_start = title_height + padding
        max_percentage = max(lang[1] for lang in languages)
        
        for i, (language, percentage) in enumerate(languages):
            y = y_start + (i * (bar_height + 10))
            bar_width = (percentage / max_percentage) * (chart_width - 100)
            
            # Get language color
            if language == "Other":
                lang_color = "#858585"  # Gray for "Other" category
            else:
                lang_color = LANGUAGE_COLORS.get(language, DEFAULT_LANGUAGE_COLOR)
            
            # Language bar
            svg += f'''
    <rect x="{padding}" y="{y}" width="{bar_width}" height="{bar_height}" 
          fill="{lang_color}" rx="3"/>
    
    <!-- Language name -->
    <text x="{padding + bar_width + 10}" y="{y + bar_height/2 + 4}" 
          fill="{colors['text_color']}" 
          font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
          font-size="12" font-weight="500">{language}</text>
    '''
            
            # Format percentage based on decimal places
            if decimal_places == 0:
                percentage_text = f"{percentage:.0f}%"
            else:
                percentage_text = f"{percentage:.{decimal_places}f}%"
                
            svg += f'''
    <text x="{width - padding}" y="{y + bar_height/2 + 4}" text-anchor="end"
          fill="{colors['subtitle_color']}" 
          font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
          font-size="11">{percentage_text}</text>
    '''
    
    svg += '</svg>'
    return svg

async def create_top_languages_svg(username: str, theme: str = "dark", languages_count: int = 5, decimal_places: int = 1, count_other_languages: bool = False, exclude_languages: List[str] = None, width: int = 400, height: int = 300, exclude_repos: List[str] = None) -> str:
    """Main function to generate top languages SVG using GraphQL"""
    try:
        # Get top languages data using GraphQL
        languages = await get_top_languages_graphql(username, languages_count, exclude_languages, count_other_languages, exclude_repos)
        
        # Generate SVG
        svg = create_language_bar_chart(languages, theme, width, height, decimal_places)
        return svg
        
    except ValueError as e:
        # Token-related errors
        return f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" fill="#f6f8fa" stroke="#d1d5da" rx="10"/>
            <text x="{width/2}" y="{height/2 - 20}" text-anchor="middle" fill="#d73a49" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="14" font-weight="600">GitHub Token Error</text>
            <text x="{width/2}" y="{height/2}" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="12">Set GITHUB_TOKEN environment variable</text>
            <text x="{width/2}" y="{height/2 + 20}" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="11">Create token at github.com/settings/tokens</text>
        </svg>'''
    except Exception as e:
        # Other errors
        error_msg = str(e)
        if "404" in error_msg or "Not Found" in error_msg:
            error_msg = f"User '{username}' not found"
        else:
            error_msg = error_msg[:40] + "..." if len(error_msg) > 40 else error_msg
            
        return f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" fill="#f6f8fa" stroke="#d1d5da" rx="10"/>
            <text x="{width/2}" y="{height/2 - 10}" text-anchor="middle" fill="#d73a49" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="14" font-weight="600">Error generating languages chart</text>
            <text x="{width/2}" y="{height/2 + 10}" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="12">{error_msg}</text>
        </svg>'''
