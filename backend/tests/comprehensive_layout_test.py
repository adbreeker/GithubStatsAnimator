#!/usr/bin/env python3
"""
Test script for comprehensive layout improvements and analysis
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from utils.account_general_generator import create_account_general_svg

async def main():
    """Test comprehensive layout improvements"""
    
    # Test username
    username = "torvalds"
    
    # Test cases with different aspects
    test_cases = [
        # Aspect ratio tests
        (500, 200, "standard"),      # 2.5:1 ratio
        (400, 200, "square-ish"),    # 2:1 ratio  
        (600, 200, "wide"),          # 3:1 ratio
        (400, 300, "tall"),          # 1.33:1 ratio
        
        # Size tests
        (300, 150, "small"),         # Small card
        (800, 300, "large"),         # Large card
        
        # Edge cases
        (350, 180, "compact"),       # Tight fit
        (700, 250, "spacious"),      # Lots of space
    ]
    
    # Different icon types to test
    icon_tests = ["github", "user", "streak", "github+user"]
    
    # Output directory (absolute path)
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Testing comprehensive layout improvements...")
    print(f"Output directory: {output_dir}")
    
    # Test different card dimensions
    for width, height, name in test_cases:
        print(f"Testing {name} layout ({width}x{height})...")
        
        try:
            # Test with default icon
            svg_content = await create_account_general_svg(
                username=username,
                icon="github",
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme="dark",
                width=width,
                height=height
            )
            
            # Save the result
            output_path = os.path.join(output_dir, f"layout_improved_{name}_{width}x{height}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error for {name}: {e}")
    
    # Test different icon types with standard dimensions
    print(f"\nTesting different icon types...")
    for icon in icon_tests:
        print(f"Testing {icon} icon...")
        
        try:
            svg_content = await create_account_general_svg(
                username=username,
                icon=icon,
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme="dark",
                width=500,
                height=200
            )
            
            # Save the result
            output_path = os.path.join(output_dir, f"icon_test_{icon.replace('+', '_plus_')}_500x200.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error for {icon}: {e}")
    
    print("\nAll comprehensive layout tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
