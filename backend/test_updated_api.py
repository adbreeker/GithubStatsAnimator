"""
Test script for the updated top languages API
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.top_languages_generator import create_top_languages_svg

# Load environment variables
load_dotenv()

async def test_top_languages_api():
    """Test the updated top languages API functionality"""
    
    # Test parameters
    username = os.getenv('GITHUB_USERNAME', 'octocat')
    
    print("Testing updated Top Languages API...")
    print(f"Username: {username}")
    print("-" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Default parameters",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 5,
                "decimal_places": 1,
                "count_other_languages": False,
                "exclude_languages": [],
                "width": 400,
                "height": 300
            }
        },
        {
            "name": "With 'Other' category",
            "params": {
                "username": username,
                "theme": "light",
                "languages_count": 3,
                "decimal_places": 2,
                "count_other_languages": True,
                "exclude_languages": [],
                "width": 500,
                "height": 400
            }
        },
        {
            "name": "Exclude JavaScript, no decimal places",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 4,
                "decimal_places": 0,
                "count_other_languages": False,
                "exclude_languages": ["JavaScript", "HTML"],
                "width": 600,
                "height": 350
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Parameters: {test_case['params']}")
        
        try:
            svg_content = await create_top_languages_svg(**test_case['params'])
            print(f"✓ SVG generated successfully ({len(svg_content)} characters)")
            
            # Save test output
            filename = f"test_output_{i}.svg"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✓ Saved to {filename}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    asyncio.run(test_top_languages_api())
