"""
Test the new top languages API parameters
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

async def test_new_parameters():
    """Test new parameters added to the top languages API"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"🧪 Testing new parameters for: {username}")
    
    # Ensure results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    test_cases = [
        {
            "name": "with_other_category",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 3,
                "count_other_languages": True,
                "decimal_places": 2
            }
        },
        {
            "name": "exclude_js_html",
            "params": {
                "username": username,
                "theme": "light", 
                "languages_count": 5,
                "exclude_languages": ["JavaScript", "HTML"],
                "decimal_places": 0
            }
        },
        {
            "name": "high_precision",
            "params": {
                "username": username,
                "theme": "dark",
                "languages_count": 4,
                "decimal_places": 3,
                "width": 500,
                "height": 400
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']}")
        try:
            svg = await create_top_languages_svg(**test_case['params'])
            
            output_path = os.path.join(results_dir, f"new_params_{test_case['name']}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            if "error" in svg.lower():
                print(f"   ⚠️ Possible error in output")
                print(f"   First 200 chars: {svg[:200]}")
            else:
                print(f"   ✅ Success: {len(svg):,} chars → tests/results/new_params_{test_case['name']}.svg")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n🎯 New parameter tests complete!")

if __name__ == "__main__":
    asyncio.run(test_new_parameters())
