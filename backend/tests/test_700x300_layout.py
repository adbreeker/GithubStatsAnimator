#!/usr/bin/env python3
"""
Test script for the new 700x300 layout with larger icon centered with 3rd stat row
"""

import asyncio
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.account_general_generator import create_account_general_svg

async def test_700x300_layout():
    """Test the new 700x300 layout with various configurations"""
    
    print("Testing 700x300 layout with larger icon centered with 3rd stat row...")
    
    username = "octocat"
    test_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(test_dir, exist_ok=True)
    
    # Test configurations
    test_configs = [
        {
            "name": "dark_github_icon",
            "icon": "github",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "light_user_avatar",
            "icon": "user",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'code_reviews'],
            "theme": "light"
        },
        {
            "name": "streak_icon",
            "icon": "streak",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'external_contributions'],
            "theme": "dark"
        },
        {
            "name": "coin_flip_animation",
            "icon": "github+user",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "with_empty_slots",
            "icon": "user",
            "slots": ['stars', None, 'commits_year', None, 'issues'],
            "theme": "light"
        }
    ]
    
    for config in test_configs:
        print(f"\nGenerating {config['name']} (700x300)...")
        
        try:
            svg = await create_account_general_svg(
                username=username,
                icon=config["icon"],
                slots=config["slots"],
                theme=config["theme"]
            )
            
            # Save to file
            output_file = os.path.join(test_dir, f"700x300_{config['name']}.svg")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"✓ Generated: {output_file}")
            
            # Verify SVG dimensions
            if 'width="700"' in svg and 'height="300"' in svg:
                print("✓ Correct dimensions: 700x300")
            else:
                print("✗ Incorrect dimensions!")
            
            # Verify viewBox
            if 'viewBox="0 0 700 300"' in svg:
                print("✓ Correct viewBox: 0 0 700 300")
            else:
                print("✗ Incorrect viewBox!")
            
            # Check for proper icon positioning (icon should be around x=60, large size)
            if 'transform="translate(60,' in svg or 'x="60"' in svg:
                print("✓ Icon positioned on left side")
            else:
                print("! Icon positioning may need verification")
            
            # Check for proper stats positioning (should be further right)
            if 'x="220"' in svg and 'x="420"' in svg:
                print("✓ Stats positioned in right area")
            else:
                print("! Stats positioning may need verification")
                
        except Exception as e:
            print(f"✗ Error generating {config['name']}: {e}")
    
    print(f"\n✓ All test SVGs saved to: {test_dir}")
    print("Open the SVG files in a browser to verify the 700x300 layout!")

if __name__ == "__main__":
    asyncio.run(test_700x300_layout())
