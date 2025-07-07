"""
Quick Test Script - Fast SVG Generation Tests
For rapid testing during development
"""
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.contributions_graph_generator import generate_contributions_svg
from utils.top_languages_generator import create_top_languages_svg
from utils.account_general_generator import create_account_general_svg

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
        # First, fetch and display the raw contributions data
        from utils.contributions_graph_generator import GitHubContributionsAPI
        
        print("📊 Fetching contributions data...")
        contrib_api = GitHubContributionsAPI()
        contrib_data = await contrib_api.fetch_contributions(username)
        
        print(f"📈 Contributions Data for {username}:")
        print(f"   📊 Total Contributions: {contrib_data.get('totalContributions', 'N/A')}")
        print(f"   📅 Weeks of data: {len(contrib_data.get('weeks', []))}")
        
        # Count contributions by level
        level_counts = {'level0': 0, 'level1': 0, 'level2': 0, 'level3': 0, 'level4': 0}
        max_day_count = 0
        
        for week in contrib_data.get('weeks', []):
            for day in week.get('contributionDays', []):
                count = day.get('contributionCount', 0)
                max_day_count = max(max_day_count, count)
                
                if count == 0:
                    level_counts['level0'] += 1
                elif count <= 2:
                    level_counts['level1'] += 1
                elif count <= 5:
                    level_counts['level2'] += 1
                elif count <= 8:
                    level_counts['level3'] += 1
                else:
                    level_counts['level4'] += 1
        
        print(f"   📊 Contribution levels:")
        print(f"      🔳 No contributions (0): {level_counts['level0']} days")
        print(f"      🟢 Light (1-2): {level_counts['level1']} days")
        print(f"      🟢 Medium (3-5): {level_counts['level2']} days")
        print(f"      🟢 High (6-8): {level_counts['level3']} days")
        print(f"      🟢 Very High (9+): {level_counts['level4']} days")
        print(f"   🔥 Max contributions in a day: {max_day_count}")
        
        # Now generate the SVG
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
        # First, fetch and display the raw language data
        from utils.top_languages_generator import GitHubLanguagesGraphQL
        
        print("📊 Fetching language statistics...")
        lang_api = GitHubLanguagesGraphQL()
        raw_data = await lang_api.fetch_top_languages_graphql(username)
        
        # Process the data to get language aggregation (similar to what the SVG generator does internally)
        lang_stats = {}
        total_size = 0
        
        for repo in raw_data:
            for edge in repo['languages']['edges']:
                lang_name = edge['node']['name']
                size = edge['size']
                lang_stats[lang_name] = lang_stats.get(lang_name, 0) + size
                total_size += size
        
        # Sort languages by size
        sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
        
        print(f"📈 Language Data for {username}:")
        if sorted_langs:
            for i, (lang, size) in enumerate(sorted_langs[:8], 1):
                percentage = (size / total_size * 100) if total_size > 0 else 0
                print(f"   {i}. {lang}: {size:,} bytes ({percentage:.1f}%)")
        else:
            print("   No language data available")
        
        print(f"   📦 Total repositories analyzed: {len(raw_data)}")
        print(f"   📊 Total code size: {total_size:,} bytes")
        print(f"   💻 Total languages found: {len(sorted_langs)}")
        
        # Now generate the SVG
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
    
    # Test 3: Account general stats
    print("\n3️⃣ Testing account general stats...")
    try:
        # First, fetch and display the raw stats data
        from utils.account_general_generator import GitHubAccountStatsAPI, calculate_basic_stats
        
        print("📊 Fetching raw statistics...")
        api = GitHubAccountStatsAPI()
        user_data = await api.fetch_account_stats(username)
        stats = calculate_basic_stats(user_data)
        
        # Get enhanced stats (including streak)
        total_commits = await api.fetch_total_commits(username)
        total_reviews = await api.fetch_total_code_reviews(username)
        streak = await api.calculate_streak(user_data['contributionsCollection']['contributionCalendar'])
        
        # Update stats with comprehensive data
        stats['commits_total'] = total_commits
        stats['code_reviews'] = total_reviews
        stats['streak'] = streak
        
        print(f"📈 Complete API Stats for {username}:")
        print(f"   👤 Username: {user_data.get('login', 'N/A')}")
        print(f"   📅 Account Created: {user_data.get('createdAt', 'N/A')[:10]}")
        print(f"   ⭐ Total Stars: {stats['stars']}")
        print(f"   📝 Total Commits (All-Time): {stats['commits_total']}")
        print(f"   📅 Commits ({datetime.now().year}): {stats['commits_year']}")
        print(f"   🔀 Pull Requests (All-Time): {stats['pull_requests']}")
        print(f"   👀 Code Reviews (All-Time): {stats['code_reviews']}")
        print(f"   🐛 Issues (All-Time): {stats['issues']}")
        print(f"   🌐 External Contributions: {stats['external_contributions']}")
        print(f"   🔥 Current Streak: {streak} days")
        print(f"   👥 Followers: {stats.get('followers', 'N/A')}")
        print(f"   👤 Following: {stats.get('following', 'N/A')}")
        print(f"   📦 Public Repos: {stats.get('public_repos', 'N/A')}")
        
        # API validation checks
        print("\n🔍 API Validation Checks:")
        checks_passed = 0
        total_checks = 0
        
        # Check 1: Total commits should be >= current year commits
        total_checks += 1
        if total_commits >= stats['commits_year']:
            print(f"   ✅ Total commits ({total_commits}) >= year commits ({stats['commits_year']})")
            checks_passed += 1
        else:
            print(f"   ❌ Total commits ({total_commits}) < year commits ({stats['commits_year']})")
        
        # Check 2: Code reviews should be non-negative
        total_checks += 1
        if total_reviews >= 0:
            print(f"   ✅ Code reviews count is valid ({total_reviews})")
            checks_passed += 1
        else:
            print(f"   ❌ Code reviews count is negative ({total_reviews})")
        
        # Check 3: Streak should be non-negative
        total_checks += 1
        if streak >= 0:
            print(f"   ✅ Streak value is valid ({streak} days)")
            checks_passed += 1
        else:
            print(f"   ❌ Streak value is negative ({streak} days)")
        
        # Check 4: Essential data is present
        total_checks += 1
        if user_data.get('login') and stats.get('stars') is not None:
            print(f"   ✅ Essential data present (login: {user_data.get('login')})")
            checks_passed += 1
        else:
            print(f"   ❌ Missing essential data")
        
        print(f"\n📊 Validation Summary: {checks_passed}/{total_checks} checks passed")
        
        # Now generate the SVG with comprehensive stats
        print(f"\n🎨 Generating SVG with comprehensive stats...")
        svg = await create_account_general_svg(
            username=username,
            theme="dark",
            icon="default+streak",
            slots=['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues', 'code_reviews']
        )
        
        output_path = os.path.join(results_dir, f"quick_account_{username}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        # Check for errors
        if "error" in svg.lower():
            print(f"⚠️ Account general: Possible error in output")
            print("First 200 chars:", svg[:200])
        else:
            print(f"✅ Account general: {len(svg):,} chars → tests/results/quick_account_{username}.svg")
        
    except Exception as e:
        print(f"❌ Account general failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎯 Quick test complete!")

if __name__ == "__main__":
    asyncio.run(quick_test())
