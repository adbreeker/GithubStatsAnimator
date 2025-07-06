#!/usr/bin/env python3
"""
Debug user icon issue
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from utils.account_general_generator import create_account_general_svg, GitHubAccountStatsAPI

async def debug_user_icon():
    """Debug why user icon is not showing"""
    
    # Test username
    username = "torvalds"
    
    print(f"Debugging user icon for {username}...")
    
    # First, let's fetch user data to see if avatar URL is being retrieved
    try:
        api = GitHubAccountStatsAPI()
        user_data = await api.fetch_account_stats(username)
        avatar_url = user_data.get('avatarUrl')
        print(f"Avatar URL: {avatar_url}")
        
        if avatar_url:
            # Try to fetch the avatar
            from utils.account_general_generator import fetch_avatar_as_data_uri
            data_uri = await fetch_avatar_as_data_uri(avatar_url)
            if data_uri:
                print(f"Avatar fetch successful, data URI length: {len(data_uri)}")
            else:
                print("Avatar fetch failed")
        else:
            print("No avatar URL found")
    
    except Exception as e:
        print(f"Error fetching user data: {e}")
    
    # Test the icon generation directly
    try:
        from utils.account_general_generator import get_icon_svg
        icon_svg = await get_icon_svg("user", username, "dark", 50, 50, avatar_url, 80)
        print(f"Generated icon SVG length: {len(icon_svg)}")
        print(f"Icon SVG preview: {icon_svg[:200]}...")
        
    except Exception as e:
        print(f"Error generating icon: {e}")

if __name__ == "__main__":
    asyncio.run(debug_user_icon())
