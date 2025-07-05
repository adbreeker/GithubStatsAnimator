"""
Test responsive SVG sizing for top languages
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

async def test_responsive_sizing():
    """Test responsive sizing with different dimensions"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"🎨 Testing responsive sizing for: {username}")
    
    # Ensure results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    test_cases = [
        {
            "name": "small_compact",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 5,
                "width": 250,
                "height": 200,
                "decimal_places": 1
            }
        },
        {
            "name": "wide_short",
            "params": {
                "username": username,
                "theme": "light",
                "languages_count": 8,
                "width": 800,
                "height": 300,
                "decimal_places": 2,
                "count_other_languages": True
            }
        },
        {
            "name": "narrow_tall",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 10,
                "width": 300,
                "height": 600,
                "decimal_places": 0
            }
        },
        {
            "name": "large_detailed",
            "params": {
                "username": username,
                "theme": "light",
                "languages_count": 8,
                "width": 700,
                "height": 500,
                "decimal_places": 4,
                "count_other_languages": True,
                "exclude_languages": ["Tcl"]
            }
        },
        {
            "name": "tiny_minimal", 
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 3,
                "width": 200,
                "height": 150,
                "decimal_places": 0
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']} ({test_case['params']['width']}x{test_case['params']['height']})")
        try:
            svg = await create_top_languages_svg(**test_case['params'])
            
            output_path = os.path.join(results_dir, f"responsive_{test_case['name']}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            if "error" in svg.lower():
                print(f"   ⚠️ Possible error in output")
                print(f"   First 200 chars: {svg[:200]}")
            else:
                print(f"   ✅ Success: {len(svg):,} chars → tests/results/responsive_{test_case['name']}.svg")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n🎯 Responsive sizing tests complete!")
    print("\n📖 Check the generated SVG files to see how they adapt to different sizes:")
    for test_case in test_cases:
        params = test_case['params']
        print(f"   • {test_case['name']}: {params['width']}x{params['height']} pixels")

if __name__ == "__main__":
    asyncio.run(test_responsive_sizing())
