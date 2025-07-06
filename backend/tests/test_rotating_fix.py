#!/usr/bin/env python3
"""
Test script for the fixed rotating icon with pre-flipped second side
"""

import asyncio
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.account_general_generator import create_account_general_svg

async def test_rotating_icon_fix():
    """Test the rotating icon with pre-flipped second side"""
    
    print("Testing rotating icon fix with pre-flipped second side...")
    
    username = "octocat"
    test_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(test_dir, exist_ok=True)
    
    # Test different rotating configurations
    test_configs = [
        {
            "name": "rotating_github_user",
            "icon": "github+user",
            "slots": ['stars', 'commits_year', 'pull_requests', 'issues', None],
            "theme": "dark"
        },
        {
            "name": "rotating_user_streak",
            "icon": "user+streak",
            "slots": ['stars', 'commits_total', 'pull_requests', None, 'external_contributions'],
            "theme": "light"
        },
        {
            "name": "rotating_github_streak",
            "icon": "github+streak",
            "slots": ['stars', None, 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        }
    ]
    
    for config in test_configs:
        print(f"\nGenerating {config['name']}...")
        
        try:
            svg = await create_account_general_svg(
                username=username,
                icon=config["icon"],
                slots=config["slots"],
                theme=config["theme"]
            )
            
            # Save to file
            output_file = os.path.join(test_dir, f"fixed_{config['name']}.svg")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"✓ Generated: {output_file}")
            
            # Check for the pre-flip transform
            if 'scaleX(-1)' in svg and f'translate(-{80}' in svg:
                print("✓ Second side properly pre-flipped")
            else:
                print("! Pre-flip transform may need verification")
                
        except Exception as e:
            print(f"✗ Error generating {config['name']}: {e}")
    
    print(f"\n✓ All rotating icon test SVGs saved to: {test_dir}")
    print("Open the SVG files in a browser to verify the rotation animation looks correct!")

if __name__ == "__main__":
    asyncio.run(test_rotating_icon_fix())
