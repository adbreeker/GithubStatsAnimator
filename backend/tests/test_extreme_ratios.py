"""
Test extreme aspect ratios for SVG responsiveness
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.top_languages_generator import create_top_languages_svg

async def test_extreme_ratios():
    """Test extreme aspect ratios"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"🔬 Testing extreme aspect ratios for: {username}")
    
    # Ensure results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    test_cases = [
        {
            "name": "ultra_wide",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 8,
                "width": 1000,
                "height": 200,
                "decimal_places": 1,
                "count_other_languages": True
            }
        },
        {
            "name": "very_tall",
            "params": {
                "username": username,
                "theme": "light",
                "languages_count": 12,
                "width": 250,
                "height": 800,
                "decimal_places": 0
            }
        },
        {
            "name": "square_large",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 6,
                "width": 500,
                "height": 500,
                "decimal_places": 2
            }
        },
        {
            "name": "very_small",
            "params": {
                "username": username,
                "theme": "light",
                "languages_count": 3,
                "width": 150,
                "height": 120,
                "decimal_places": 0
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']} ({test_case['params']['width']}x{test_case['params']['height']})")
        try:
            svg = await create_top_languages_svg(**test_case['params'])
            
            output_path = os.path.join(results_dir, f"extreme_{test_case['name']}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"   ✅ Success: {len(svg):,} chars → tests/results/extreme_{test_case['name']}.svg")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n🎯 Extreme ratio tests complete!")

if __name__ == "__main__":
    asyncio.run(test_extreme_ratios())
