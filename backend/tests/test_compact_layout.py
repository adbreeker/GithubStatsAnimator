#!/usr/bin/env python3
"""
Test script for the new compact 400x200 layout with title/stats on left, logo on right
"""

import asyncio
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.account_general_generator import create_account_general_svg

async def test_compact_layout():
    """Test the new compact 400x200 layout"""
    
    print("Testing compact 400x200 layout with left stats, right logo...")
    
    username = "octocat"
    test_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(test_dir, exist_ok=True)
    
    # Test configurations
    test_configs = [
        {
            "name": "compact_dark_github",
            "icon": "github",
            "slots": ['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
            "theme": "dark"
        },
        {
            "name": "compact_light_user",
            "icon": "user",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'code_reviews'],
            "theme": "light"
        },
        {
            "name": "compact_streak",
            "icon": "streak",
            "slots": ['stars', 'commits_year', 'pull_requests', None, 'issues'],
            "theme": "dark"
        },
        {
            "name": "compact_animation",
            "icon": "github+user",
            "slots": ['stars', 'commits_total', None, 'pull_requests', 'issues'],
            "theme": "light"
        }
    ]
    
    for config in test_configs:
        print(f"\nGenerating {config['name']} (400x200)...")
        
        try:
            svg = await create_account_general_svg(
                username=username,
                icon=config["icon"],
                slots=config["slots"],
                theme=config["theme"]
            )
            
            # Save to file
            output_file = os.path.join(test_dir, f"{config['name']}.svg")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"✓ Generated: {output_file}")
            
            # Verify SVG dimensions
            if 'width="400"' in svg and 'height="200"' in svg:
                print("✓ Correct dimensions: 400x200")
            else:
                print("✗ Incorrect dimensions!")
            
            # Verify viewBox
            if 'viewBox="0 0 400 200"' in svg:
                print("✓ Correct viewBox: 0 0 400 200")
            else:
                print("✗ Incorrect viewBox!")
            
            # Check for left-aligned title (small x position)
            if any(f'x="{x}"' in svg for x in range(20, 50)):
                print("✓ Title positioned on left side")
            else:
                print("! Title positioning may need verification")
            
            # Check for right-side icon positioning
            if any(f'translate({x},' in svg for x in range(300, 350)):
                print("✓ Icon positioned on right side")
            else:
                print("! Icon positioning may need verification")
                
        except Exception as e:
            print(f"✗ Error generating {config['name']}: {e}")
    
    print(f"\n✓ All test SVGs saved to: {test_dir}")
    print("Open the SVG files in a browser to verify the new compact layout!")

if __name__ == "__main__":
    asyncio.run(test_compact_layout())
