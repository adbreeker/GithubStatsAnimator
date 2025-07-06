#!/usr/bin/env python3
"""
Test script for layout centering and responsiveness improvements
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from utils.account_general_generator import create_account_general_svg

async def main():
    """Test different card dimensions for proper centering"""
    
    # Test username
    username = "torvalds"
    
    # Different card dimensions to test
    test_cases = [
        # (width, height, name)
        (400, 180, "compact"),
        (500, 200, "standard"),
        (600, 220, "wide"),
        (450, 250, "tall"),
        (350, 160, "small"),
        (700, 280, "large"),
    ]
    
    # Output directory (absolute path)
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Testing layout centering and responsiveness...")
    print(f"Output directory: {output_dir}")
    
    for width, height, name in test_cases:
        print(f"Testing {name} layout ({width}x{height})...")
        
        try:
            # Test with different configurations
            svg_content = await create_account_general_svg(
                username=username,
                icon="github",
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme="dark",
                width=width,
                height=height
            )
            
            # Save the result
            output_path = os.path.join(output_dir, f"centering_test_{name}_{width}x{height}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error for {name}: {e}")
    
    print("\nAll centering tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
