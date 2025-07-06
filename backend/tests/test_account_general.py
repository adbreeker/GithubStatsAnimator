"""
Account General Stats Test Script
Tests the new account general stats SVG generator with various configurations
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.account_general_generator import create_account_general_svg

async def test_account_general():
    """Test account general stats with different configurations"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"🚀 Account General Stats Test for: {username}")
    
    # Ensure results directory exists (absolute path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    print(f"📁 Results will be saved to: {results_dir}")
    
    test_configs = [
        {
            "name": "default",
            "icon": "default",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "github_icon",
            "icon": "github", 
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "streak_icon",
            "icon": "streak",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "rotating_default_github",
            "icon": "default+github",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "rotating_github_streak",
            "icon": "github+streak",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "dark"
        },
        {
            "name": "light_theme",
            "icon": "default",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues'],
            "theme": "light"
        },
        {
            "name": "all_stats",
            "icon": "default",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'code_reviews'],
            "theme": "dark"
        },
        {
            "name": "external_focus",
            "icon": "github",
            "slots": ['external_contributions', 'code_reviews', 'issues', 'pull_requests', 'stars'],
            "theme": "dark"
        },
        {
            "name": "small_size",
            "icon": "default",
            "slots": ['stars', 'commits_year', 'pull_requests'],
            "theme": "dark",
            "width": 300,
            "height": 150
        },
        {
            "name": "large_size",
            "icon": "default+streak",
            "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'external_contributions'],
            "theme": "dark", 
            "width": 600,
            "height": 250
        }
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{i}️⃣ Testing: {config['name']}")
        try:
            # Extract width and height if provided
            width = config.get('width', 400)
            height = config.get('height', 200)
            
            svg = await create_account_general_svg(
                username=username,
                icon=config['icon'],
                slots=config['slots'],
                theme=config['theme'],
                width=width,
                height=height
            )
            
            output_path = os.path.join(results_dir, f"account_general_{config['name']}_{username}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            # Basic validation
            if len(svg) < 100:
                print(f"⚠️ {config['name']}: SVG too short ({len(svg)} chars)")
                print("Content:", svg[:100])
                failed_tests += 1
            elif "error" in svg.lower():
                print(f"⚠️ {config['name']}: Possible error in output")
                print("First 200 chars:", svg[:200])
                failed_tests += 1
            else:
                print(f"✅ {config['name']}: {len(svg):,} chars → account_general_{config['name']}_{username}.svg")
                successful_tests += 1
                
                # Print config details
                print(f"   📊 Icon: {config['icon']}, Theme: {config['theme']}, Size: {width}x{height}")
                print(f"   📈 Stats: {', '.join(config['slots'])}")
        
        except Exception as e:
            print(f"❌ {config['name']} failed: {str(e)[:100]}")
            failed_tests += 1
    
    # Summary
    print(f"\n🎯 Test Summary:")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📁 Results saved to: {results_dir}")
    
    if failed_tests == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️ {failed_tests} tests failed - check error messages above")

async def test_individual_stats():
    """Test individual stat types to ensure they all work"""
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    print(f"\n🔍 Individual Stats Test for: {username}")
    
    # Ensure results directory exists (absolute path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    
    stat_types = [
        'stars', 'commits_total', 'commits_year', 'pull_requests', 
        'code_reviews', 'issues', 'external_contributions'
    ]
    
    for stat in stat_types:
        print(f"\n🔬 Testing stat: {stat}")
        try:
            svg = await create_account_general_svg(
                username=username,
                icon="default",
                slots=[stat, stat, stat, stat, stat],  # All slots same stat
                theme="dark"
            )
            
            output_path = os.path.join(results_dir, f"stat_test_{stat}_{username}.svg")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"✅ {stat}: {len(svg):,} chars → stat_test_{stat}_{username}.svg")
        
        except Exception as e:
            print(f"❌ {stat} failed: {str(e)[:100]}")

if __name__ == "__main__":
    print("Starting Account General Stats Tests...\n")
    asyncio.run(test_account_general())
    asyncio.run(test_individual_stats())
    print("\n✨ All tests completed!")
