#!/usr/bin/env python3
"""
Test script for fixed size layout (500x300)
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from utils.account_general_generator import create_account_general_svg

async def main():
    """Test the new fixed size layout"""
    
    # Test username
    username = "torvalds"
    
    # Output directory (absolute path)
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Testing fixed size layout (500x300)...")
    print(f"Output directory: {output_dir}")
    
    # Test different configurations
    test_configs = [
        # (theme, icon, name)
        ("dark", "github", "dark_github"),
        ("light", "github", "light_github"),
        ("dark", "user", "dark_user"),
        ("dark", "streak", "dark_streak"),
        ("dark", "github+user", "dark_flip"),
    ]
    
    for theme, icon, name in test_configs:
        print(f"Testing {name}...")
        
        try:
            svg_content = await create_account_general_svg(
                username=username,
                icon=icon,
                slots=['stars', 'commits_year', 'pull_requests', 'issues', 'external_contributions'],
                theme=theme
            )
            
            # Save the result
            output_path = os.path.join(output_dir, f"fixed_size_{name}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"  ✓ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error for {name}: {e}")
    
    print("\nAll fixed size tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
