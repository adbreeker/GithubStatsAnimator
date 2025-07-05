"""
Quick Test Script - Fast SVG Generation Tests
For rapid testing during development
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.contributions_graph_generator import generate_contributions_svg
from utils.top_languages_generator import create_top_languages_svg

async def quick_test():
    """Quick test of both SVG generators"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"🚀 Quick test for: {username}")
    
    # Ensure results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Test 1: Simple contribution graph
    print("\n1️⃣ Testing contribution graph...")
    try:
        svg = await generate_contributions_svg(
            username=username,
            theme="dark",
            text="TEST",
            animation_time=1.0
        )
        
        output_path = os.path.join(results_dir, f"quick_contrib_{username}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✅ Contribution graph: {len(svg):,} chars → tests/results/quick_contrib_{username}.svg")
        
    except Exception as e:
        print(f"❌ Contribution graph failed: {e}")
    
    # Test 2: Simple top languages
    print("\n2️⃣ Testing top languages...")
    try:
        svg = await create_top_languages_svg(
            username=username,
            theme="dark",
            languages_count=5
        )
        
        output_path = os.path.join(results_dir, f"quick_langs_{username}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        # Check for errors
        if "error" in svg.lower():
            print(f"⚠️ Top languages: Possible error in output")
            print("First 200 chars:", svg[:200])
        else:
            print(f"✅ Top languages: {len(svg):,} chars → tests/results/quick_langs_{username}.svg")
        
    except Exception as e:
        print(f"❌ Top languages failed: {e}")
    
    print("\n🎯 Quick test complete!")

if __name__ == "__main__":
    asyncio.run(quick_test())
