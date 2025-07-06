#!/usr/bin/env python3
"""
Test script for final layout improvements and edge cases
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from utils.account_general_generator import create_account_general_svg

async def main():
    """Test final layout improvements with edge cases"""
    
    # Test username
    username = "torvalds"
    
    # Edge case tests for width and height
    test_cases = [
        # Very wide cards
        (800, 200, "very_wide"),
        (900, 220, "ultra_wide"),
        
        # Very tall cards
        (400, 300, "tall"),
        (350, 350, "square"),
        
        # Very small cards
        (300, 140, "tiny"),
        (320, 160, "small"),
        
        # Extreme ratios
        (600, 180, "extreme_wide"),
        (300, 250, "extreme_tall"),
        
        # Standard but different sizes
        (450, 190, "compact_std"),
        (550, 210, "large_std"),
    ]
    
    # Output directory (absolute path)
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Testing final layout improvements and edge cases...")
    print(f"Output directory: {output_dir}")
    
    for width, height, name in test_cases:
        print(f"Testing {name} layout ({width}x{height})...")
        
        try:
            # Test with standard configuration
            svg_content = await create_account_general_svg(
                username=username,
                icon="github",
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme="dark",
                width=width,
                height=height
            )
            
            # Save the result
            output_path = os.path.join(output_dir, f"final_{name}_{width}x{height}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error for {name}: {e}")
    
    # Test light theme with a few sizes
    print(f"\nTesting light theme...")
    for width, height, name in [("400", "180", "compact"), ("500", "200", "standard"), ("600", "220", "wide")]:
        try:
            svg_content = await create_account_general_svg(
                username=username,
                icon="user",
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme="light",
                width=int(width),
                height=int(height)
            )
            
            output_path = os.path.join(output_dir, f"final_light_{name}_{width}x{height}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Light theme {name}: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Light theme error for {name}: {e}")
    
    print("\nAll final layout tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
