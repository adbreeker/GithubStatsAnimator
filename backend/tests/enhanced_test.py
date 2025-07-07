"""
Enhanced Local Test Script for GitHub Stats APIs
Comprehensive testing suite for SVG generation without starting the Flask server
"""
import asyncio
import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.contributions_graph_generator import generate_contributions_svg
from utils.top_languages_generator import create_top_languages_svg
from utils.account_general_generator import create_account_general_svg, GitHubAccountStatsAPI, calculate_basic_stats

class TestRunner:
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.results_dir = os.path.join(os.path.dirname(__file__), 'results')
        
    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️", "test": "🔄"}
        print(f"[{timestamp}] {icons.get(level, '•')} {message}")
    
    def save_result(self, test_name, success, details=None):
        self.results[test_name] = {
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

async def test_contribution_graph_basic(runner):
    """Test basic contribution graph generation"""
    runner.log("Testing Basic Contribution Graph...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    try:
        svg_content = await generate_contributions_svg(
            username=username,
            theme="dark",
            text="TEST",
            line_color="#ff8c00",
            line_alpha=0.7,
            square_size=11,
            animation_time=2.0,  # Shorter for testing
            pause_time=0.0
        )
        
        filename = os.path.join(runner.results_dir, f"{username}_contrib_basic.svg")
        os.makedirs(runner.results_dir, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        runner.log(f"Basic contribution graph saved: tests/results/{username}_contrib_basic.svg", "success")
        runner.log(f"SVG size: {len(svg_content):,} characters")
        runner.save_result("contribution_graph_basic", True, {
            "filename": f"tests/results/{username}_contrib_basic.svg",
            "size": len(svg_content),
            "username": username
        })
        return True
        
    except Exception as e:
        runner.log(f"Basic contribution graph failed: {e}", "error")
        runner.save_result("contribution_graph_basic", False, {"error": str(e)})
        return False

async def test_contribution_graph_advanced(runner):
    """Test contribution graph with various parameters"""
    runner.log("Testing Advanced Contribution Graph Parameters...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    test_configs = [
        {
            "name": "light_theme",
            "params": {"theme": "light", "text": "LIGHT", "line_color": "#0066cc"},
        },
        {
            "name": "custom_text",
            "params": {"theme": "dark", "text": "GITHUB", "line_color": "#ff6b6b"},
        },
        {
            "name": "large_squares",
            "params": {"theme": "dark", "text": "BIG", "square_size": 15},
        },
        {
            "name": "transparent_lines",
            "params": {"theme": "dark", "text": "FADE", "line_alpha": 0.3},
        }
    ]
    
    success_count = 0
    
    for config in test_configs:
        try:
            runner.log(f"  Testing {config['name']}...")
            
            svg_content = await generate_contributions_svg(
                username=username,
                animation_time=1.0,  # Quick test
                **config["params"]
            )
            
            filename = os.path.join(runner.results_dir, f"{username}_contrib_{config['name']}.svg")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            runner.log(f"  ✅ {config['name']}: {len(svg_content):,} chars")
            success_count += 1
            
        except Exception as e:
            runner.log(f"  ❌ {config['name']}: {e}")
    
    success = success_count == len(test_configs)
    runner.save_result("contribution_graph_advanced", success, {
        "total_tests": len(test_configs),
        "passed": success_count
    })
    
    return success

async def test_top_languages_basic(runner):
    """Test basic top languages generation"""
    runner.log("Testing Basic Top Languages...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    try:
        svg_content = await create_top_languages_svg(
            username=username,
            theme="dark",
            languages_count=5,
            width=400,
            height=300
        )
        
        filename = os.path.join(runner.results_dir, f"{username}_langs_basic.svg")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        # Validate SVG content
        if "error" in svg_content.lower() or "GitHub Token Error" in svg_content:
            runner.log("SVG contains errors - likely authentication issue", "warning")
            runner.log("SVG preview:", "info")
            print("-" * 50)
            print(svg_content[:500] + "..." if len(svg_content) > 500 else svg_content)
            print("-" * 50)
            runner.save_result("top_languages_basic", False, {"error": "Authentication or API error"})
            return False
        
        runner.log(f"Basic top languages saved: tests/results/{username}_langs_basic.svg", "success")
        runner.log(f"SVG size: {len(svg_content):,} characters")
        runner.save_result("top_languages_basic", True, {
            "filename": f"tests/results/{username}_langs_basic.svg",
            "size": len(svg_content),
            "username": username
        })
        return True
        
    except Exception as e:
        runner.log(f"Basic top languages failed: {e}", "error")
        runner.save_result("top_languages_basic", False, {"error": str(e)})
        return False

async def test_top_languages_advanced(runner):
    """Test top languages with various configurations"""
    runner.log("Testing Advanced Top Languages Parameters...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    test_configs = [
        {
            "name": "light_theme",
            "params": {"theme": "light"},
        },
        {
            "name": "small_chart",
            "params": {"width": 250, "height": 200, "languages_count": 3},
        },
        {
            "name": "large_chart",
            "params": {"width": 600, "height": 400, "languages_count": 10},
        },
        {
            "name": "no_decimal",
            "params": {"decimal_places": 0},
        },
        {
            "name": "with_other",
            "params": {"languages_count": 3, "count_other_languages": True, "decimal_places": 2},
        },
        {
            "name": "exclude_languages",
            "params": {"exclude_languages": ["JavaScript", "HTML"], "languages_count": 5},
        }
    ]
    
    success_count = 0
    
    for config in test_configs:
        try:
            runner.log(f"  Testing {config['name']}...")
            
            svg_content = await create_top_languages_svg(
                username=username,
                **config["params"]
            )
            
            filename = os.path.join(runner.results_dir, f"{username}_langs_{config['name']}.svg")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            # Quick validation
            if "error" not in svg_content.lower() and len(svg_content) > 500:
                runner.log(f"  ✅ {config['name']}: {len(svg_content):,} chars")
                success_count += 1
            else:
                runner.log(f"  ⚠️ {config['name']}: Possible error in output")
            
        except Exception as e:
            runner.log(f"  ❌ {config['name']}: {e}")
    
    success = success_count == len(test_configs)
    runner.save_result("top_languages_advanced", success, {
        "total_tests": len(test_configs),
        "passed": success_count
    })
    
    return success

async def test_error_conditions(runner):
    """Test error handling with invalid parameters"""
    runner.log("Testing Error Conditions...", "test")
    
    error_tests = [
        {
            "name": "invalid_username",
            "test": lambda: generate_contributions_svg(username="invaliduser123456789"),
            "expect_error": True
        },
        {
            "name": "invalid_theme", 
            "test": lambda: create_top_languages_svg(username="adbreeker", theme="invalid"),
            "expect_error": True
        }
    ]
    
    passed_tests = 0
    
    for test in error_tests:
        try:
            runner.log(f"  Testing {test['name']}...")
            result = await test["test"]()
            
            if test["expect_error"]:
                runner.log(f"  ⚠️ {test['name']}: Expected error but got result")
            else:
                runner.log(f"  ✅ {test['name']}: Success")
                passed_tests += 1
                
        except Exception as e:
            if test["expect_error"]:
                runner.log(f"  ✅ {test['name']}: Correctly caught error - {str(e)[:50]}...")
                passed_tests += 1
            else:
                runner.log(f"  ❌ {test['name']}: Unexpected error - {e}")
    
    success = passed_tests == len(error_tests)
    runner.save_result("error_handling", success, {
        "total_tests": len(error_tests),
        "passed": passed_tests
    })
    
    return success

async def test_performance(runner):
    """Test performance with timing"""
    runner.log("Testing Performance...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    # Test contribution graph performance
    try:
        start_time = time.time()
        await generate_contributions_svg(
            username=username,
            theme="dark",
            text="PERF",
            animation_time=1.0
        )
        contrib_time = time.time() - start_time
        
        runner.log(f"Contribution graph generation: {contrib_time:.2f}s")
        
    except Exception as e:
        runner.log(f"Contribution graph performance test failed: {e}", "error")
        contrib_time = None
    
    # Test top languages performance
    try:
        start_time = time.time()
        await create_top_languages_svg(
            username=username,
            theme="dark",
            languages_count=5
        )
        langs_time = time.time() - start_time
        
        runner.log(f"Top languages generation: {langs_time:.2f}s")
        
    except Exception as e:
        runner.log(f"Top languages performance test failed: {e}", "error")
        langs_time = None
    
    success = contrib_time is not None and langs_time is not None
    runner.save_result("performance", success, {
        "contribution_time": contrib_time,
        "languages_time": langs_time
    })
    
    return success

def check_environment(runner):
    """Check environment configuration"""
    runner.log("Checking Environment Configuration...", "test")
    
    username = os.getenv('GITHUB_USERNAME')
    token = os.getenv('GITHUB_TOKEN')
    
    issues = []
    
    if not username:
        issues.append("GITHUB_USERNAME not set")
        runner.log("❌ GITHUB_USERNAME not found in environment", "error")
    else:
        runner.log(f"✅ Username: {username}")
    
    if not token:
        issues.append("GITHUB_TOKEN not set")
        runner.log("❌ GITHUB_TOKEN not found in environment", "error")
    else:
        masked_token = '*' * (len(token) - 4) + token[-4:] if len(token) > 4 else '****'
        runner.log(f"✅ Token found: {masked_token}")
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        runner.log("✅ .env file found")
    else:
        issues.append(".env file not found")
        runner.log("⚠️ .env file not found", "warning")
    
    runner.save_result("environment", len(issues) == 0, {
        "username": username,
        "has_token": token is not None,
        "has_env_file": os.path.exists(env_file),
        "issues": issues
    })
    
    return len(issues) == 0

async def test_account_general_basic(runner):
    """Test basic account general stats generation with data verification"""
    runner.log("Testing Basic Account General Stats...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    try:
        # First, fetch and display the raw stats data
        runner.log("📊 Fetching raw statistics for verification...")
        api = GitHubAccountStatsAPI()
        user_data = await api.fetch_account_stats(username)
        stats = calculate_basic_stats(user_data)
        
        # Get enhanced stats (including streak)
        total_commits = await api.fetch_total_commits(username)
        total_reviews = await api.fetch_total_code_reviews(username)
        streak = await api.calculate_streak(user_data['contributionsCollection']['contributionCalendar'])
        
        stats['commits_total'] = total_commits
        stats['code_reviews'] = total_reviews
        stats['streak'] = streak
        
        # Display all stats for verification
        runner.log(f"📈 Raw Stats for {username}:")
        runner.log(f"   ⭐ Stars: {stats['stars']}")
        runner.log(f"   📝 Total Commits: {stats['commits_total']}")
        runner.log(f"   📅 Commits ({datetime.now().year}): {stats['commits_year']}")
        runner.log(f"   🔀 Pull Requests: {stats['pull_requests']}")
        runner.log(f"   👀 Code Reviews: {stats['code_reviews']}")
        runner.log(f"   🐛 Issues: {stats['issues']}")
        runner.log(f"   🌐 External Contributions: {stats['external_contributions']}")
        runner.log(f"   🔥 Current Streak: {streak} days")
        
        # Generate basic SVG
        svg_content = await create_account_general_svg(
            username=username,
            theme="dark",
            icon="streak",
            slots=['stars', 'commits_total', 'commits_year', 'pull_requests', 'issues']
        )
        
        filename = os.path.join(runner.results_dir, f"{username}_account_basic.svg")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        runner.log(f"✅ Basic Account General: {len(svg_content):,} chars", "success")
        
        # Data validation
        validation_issues = []
        if stats['commits_total'] < stats['commits_year']:
            validation_issues.append("Total commits < year commits")
        if stats['commits_total'] < 50:  # Assuming active user
            validation_issues.append(f"Low total commits: {stats['commits_total']}")
        
        if validation_issues:
            runner.log(f"⚠️ Data validation issues: {', '.join(validation_issues)}", "warning")
        else:
            runner.log("✅ Data validation passed", "success")
        
        runner.save_result("account_general_basic", True, {
            "svg_size": len(svg_content),
            "stats": stats,
            "streak": streak,
            "validation_issues": validation_issues
        })
        
        return True
        
    except Exception as e:
        runner.log(f"❌ Basic Account General failed: {e}", "error")
        runner.save_result("account_general_basic", False, {"error": str(e)})
        return False

async def test_account_general_advanced(runner):
    """Test advanced account general configurations"""
    runner.log("Testing Advanced Account General Configurations...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    test_configs = [
        {
            "name": "dark_streak_icon",
            "params": {
                "theme": "dark",
                "icon": "streak", 
                "slots": ['stars', 'commits_total', 'commits_year', 'pull_requests', 'code_reviews']
            }
        },
        {
            "name": "light_rotating_icon",
            "params": {
                "theme": "light",
                "icon": "default+streak",
                "slots": ['commits_total', 'pull_requests', 'issues', 'external_contributions', 'stars']
            }
        },
        {
            "name": "github_plus_streak",
            "params": {
                "theme": "dark", 
                "icon": "github+streak",
                "slots": ['commits_year', 'code_reviews', 'pull_requests', 'commits_total', 'issues']
            }
        },
        {
            "name": "user_avatar_light",
            "params": {
                "theme": "light",
                "icon": "user",
                "slots": ['stars', 'external_contributions', 'commits_total', 'pull_requests', 'issues']
            }
        }
    ]
    
    success_count = 0
    
    for config in test_configs:
        try:
            runner.log(f"  Testing {config['name']}...")
            
            svg_content = await create_account_general_svg(
                username=username,
                **config["params"]
            )
            
            filename = os.path.join(runner.results_dir, f"{username}_account_{config['name']}.svg")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            runner.log(f"  ✅ {config['name']}: {len(svg_content):,} chars")
            success_count += 1
            
        except Exception as e:
            runner.log(f"  ❌ {config['name']}: {e}")
    
    success = success_count == len(test_configs)
    runner.save_result("account_general_advanced", success, {
        "total_tests": len(test_configs),
        "passed": success_count
    })
    
    return success

async def test_account_general_api_accuracy(runner):
    """Test API data accuracy and consistency with comprehensive validation"""
    runner.log("Testing Account General API Data Accuracy...", "test")
    
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    try:
        api = GitHubAccountStatsAPI()
        
        # Test individual API methods
        runner.log("🔍 Testing individual API methods...")
        
        # Test basic data fetch
        user_data = await api.fetch_account_stats(username)
        basic_stats = calculate_basic_stats(user_data)
        
        # Test total commits (all years)
        total_commits = await api.fetch_total_commits(username)
        
        # Test total code reviews (all years) 
        total_reviews = await api.fetch_total_code_reviews(username)
        
        # Test streak calculation
        streak = await api.calculate_streak(user_data['contributionsCollection']['contributionCalendar'])
        
        # Ensure streak is in basic_stats for consistency
        basic_stats['streak'] = streak
        
        # Test additional API methods from other generators
        runner.log("🔍 Testing cross-API integration...")
        
        # Test contributions API
        from utils.contributions_graph_generator import GitHubContributionsAPI
        contrib_api = GitHubContributionsAPI()
        contrib_data = await contrib_api.fetch_contributions(username)
        
        # Test languages API
        from utils.top_languages_generator import GitHubLanguagesGraphQL
        lang_api = GitHubLanguagesGraphQL()
        raw_lang_data = await lang_api.fetch_top_languages_graphql(username)
        
        # Process the raw data to get aggregated stats (similar to what the SVG generator does)
        lang_stats = {}
        total_size = 0
        
        for repo in raw_lang_data:
            for edge in repo['languages']['edges']:
                lang_name = edge['node']['name']
                size = edge['size']
                lang_stats[lang_name] = lang_stats.get(lang_name, 0) + size
                total_size += size
        
        # Sort languages by size
        sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
        
        # Create a lang_data structure for consistency
        lang_data = {
            'languages': [{'name': lang, 'size': size, 'percentage': (size / total_size * 100) if total_size > 0 else 0} 
                         for lang, size in sorted_langs],
            'total_repos': len(raw_lang_data),
            'total_size': total_size
        }
        
        # Display comprehensive API results
        runner.log("📊 Complete API Method Results:")
        runner.log(f"   👤 Username: {user_data.get('login', 'N/A')}")
        runner.log(f"   📅 Account Created: {user_data.get('createdAt', 'N/A')[:10]}")
        runner.log(f"   ⭐ Total Stars: {basic_stats['stars']}")
        runner.log(f"   📝 Total Commits (All-Time): {total_commits}")
        runner.log(f"   📅 Commits ({datetime.now().year}): {basic_stats['commits_year']}")
        runner.log(f"   🔀 Pull Requests (All-Time): {basic_stats['pull_requests']}")
        runner.log(f"   👀 Code Reviews (All-Time): {total_reviews}")
        runner.log(f"   🐛 Issues (All-Time): {basic_stats['issues']}")
        runner.log(f"   🌐 External Contributions: {basic_stats['external_contributions']}")
        runner.log(f"   🔥 Current Streak: {streak} days")
        runner.log(f"   👥 Followers: {basic_stats.get('followers', 'N/A')}")
        runner.log(f"   👤 Following: {basic_stats.get('following', 'N/A')}")
        runner.log(f"   📦 Public Repos: {basic_stats.get('public_repos', 'N/A')}")
        
        # Contributions data validation
        runner.log(f"   📊 Contribution Graph - Total: {contrib_data.get('totalContributions', 'N/A')}")
        runner.log(f"   📊 Contribution Graph - Weeks: {len(contrib_data.get('weeks', []))}")
        
        # Languages data validation
        if 'languages' in lang_data and lang_data['languages']:
            top_lang = lang_data['languages'][0]
            runner.log(f"   💻 Top Language: {top_lang['name']} ({top_lang['percentage']:.1f}%)")
            runner.log(f"   💻 Languages Count: {len(lang_data['languages'])}")
            runner.log(f"   📦 Analyzed Repos: {lang_data.get('total_repos', 'N/A')}")
        else:
            runner.log(f"   💻 Languages: No data available")
        
        # Comprehensive consistency checks
        issues = []
        warnings = []
        
        # Critical checks (failures)
        if total_commits < basic_stats['commits_year']:
            issues.append(f"Total commits ({total_commits}) < year commits ({basic_stats['commits_year']})")
            
        if total_reviews < 0:
            issues.append(f"Negative code reviews count: {total_reviews}")
            
        if streak < 0:
            issues.append(f"Negative streak value: {streak}")
            
        if not user_data.get('login'):
            issues.append("Missing user login data")
        
        if basic_stats['stars'] < 0:
            issues.append(f"Negative stars count: {basic_stats['stars']}")
        
        # Warning checks (suspicious but not necessarily wrong)
        if contrib_data.get('totalContributions', 0) != basic_stats['commits_year']:
            warnings.append(f"Contrib total ({contrib_data.get('totalContributions')}) != year commits ({basic_stats['commits_year']})")
        
        if total_commits > 50000:  # Very high commit count
            warnings.append(f"Extremely high commit count: {total_commits}")
        
        if streak > 365:  # Very long streak
            warnings.append(f"Very long streak: {streak} days")
        
        # Cross-API consistency
        runner.log("🔍 Cross-API Consistency Checks:")
        consistency_score = 0
        consistency_total = 0
        
        # Check 1: Basic API vs Enhanced Commits
        consistency_total += 1
        if total_commits >= basic_stats['commits_year']:
            runner.log("   ✅ Total commits >= year commits")
            consistency_score += 1
        else:
            runner.log(f"   ❌ Total commits ({total_commits}) < year commits ({basic_stats['commits_year']})")
        
        # Check 2: Code reviews validation
        consistency_total += 1
        if total_reviews >= 0:
            runner.log(f"   ✅ Code reviews count valid ({total_reviews})")
            consistency_score += 1
        else:
            runner.log(f"   ❌ Invalid code reviews count: {total_reviews}")
        
        # Check 3: Contributions graph consistency
        consistency_total += 1
        contrib_total = contrib_data.get('totalContributions', 0)
        if contrib_total >= 0:
            runner.log(f"   ✅ Contributions graph total valid ({contrib_total})")
            consistency_score += 1
        else:
            runner.log(f"   ❌ Invalid contributions total: {contrib_total}")
        
        # Check 4: Languages data consistency
        consistency_total += 1
        if lang_data and 'languages' in lang_data and isinstance(lang_data['languages'], list):
            runner.log(f"   ✅ Languages data valid ({len(lang_data['languages'])} languages)")
            consistency_score += 1
        else:
            runner.log("   ❌ Invalid languages data structure")
        
        success = len(issues) == 0
        
        if success:
            runner.log("✅ All critical API data checks passed", "success")
        else:
            runner.log(f"❌ Critical API issues: {'; '.join(issues)}", "error")
        
        if warnings:
            runner.log(f"⚠️ API warnings: {'; '.join(warnings)}", "warning")
        
        runner.log(f"📊 Consistency Score: {consistency_score}/{consistency_total}")
        
        runner.save_result("account_general_api_accuracy", success, {
            "total_commits": total_commits,
            "total_reviews": total_reviews,
            "streak": streak,
            "basic_stats": basic_stats,
            "contrib_data": contrib_data,
            "lang_data": lang_data,
            "issues": issues,
            "warnings": warnings,
            "consistency_score": f"{consistency_score}/{consistency_total}"
        })
        
        return success
        
    except Exception as e:
        runner.log(f"❌ API accuracy test failed: {e}", "error")
        import traceback
        runner.log(f"Traceback: {traceback.format_exc()}")
        runner.save_result("account_general_api_accuracy", False, {"error": str(e)})
        return False

async def main():
    """Run comprehensive test suite"""
    runner = TestRunner()
    
    print("🚀 GitHub Stats Enhanced Test Suite")
    print("=" * 60)
    
    # Check environment first
    env_ok = check_environment(runner)
    if not env_ok:
        runner.log("Environment issues detected. Some tests may fail.", "warning")
    
    print()
    
    # Run all tests
    test_functions = [
        test_contribution_graph_basic,
        test_contribution_graph_advanced,
        test_top_languages_basic,
        test_top_languages_advanced,
        test_account_general_basic,
        test_account_general_advanced,
        test_account_general_api_accuracy,
        test_error_conditions,
        test_performance
    ]
    
    for test_func in test_functions:
        try:
            await test_func(runner)
            print()
        except Exception as e:
            runner.log(f"Test {test_func.__name__} crashed: {e}", "error")
            print()
    
    # Generate summary
    total_time = time.time() - runner.start_time
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for result in runner.results.values() if result["success"])
    total = len(runner.results)
    
    for test_name, result in runner.results.items():
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status} {test_name.replace('_', ' ').title()}")
    
    print()
    print(f"📈 Results: {passed}/{total} tests passed")
    print(f"⏱️ Total time: {total_time:.2f}s")
    
    # Save detailed results
    results_file = os.path.join(runner.results_dir, "test_results.json")
    os.makedirs(runner.results_dir, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump({
            "summary": {
                "passed": passed,
                "total": total,
                "duration": total_time,
                "timestamp": datetime.now().isoformat()
            },
            "results": runner.results
        }, f, indent=2)
    
    runner.log(f"Detailed results saved to: tests/results/test_results.json")
    
    # List generated files
    print("\n📁 Generated Files:")
    if os.path.exists(runner.results_dir):
        files = sorted(os.listdir(runner.results_dir))
        for file in files:
            file_path = os.path.join(runner.results_dir, file)
            size = os.path.getsize(file_path)
            print(f"  📄 {file} ({size:,} bytes)")
    
    if passed == total:
        print("\n🎉 All tests passed! SVG generation is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        runner = TestRunner()
        
        if arg in ["contrib", "contribution"]:
            asyncio.run(test_contribution_graph_basic(runner))
        elif arg in ["langs", "languages"]:
            asyncio.run(test_top_languages_basic(runner))
        elif arg in ["perf", "performance"]:
            asyncio.run(test_performance(runner))
        elif arg in ["env", "environment"]:
            check_environment(runner)
        elif arg in ["errors", "error"]:
            asyncio.run(test_error_conditions(runner))
        else:
            print("Available test modes:")
            print("  python enhanced_test.py              # Run all tests")
            print("  python enhanced_test.py contrib      # Test contribution graph")
            print("  python enhanced_test.py langs        # Test top languages")
            print("  python enhanced_test.py perf         # Test performance")
            print("  python enhanced_test.py env          # Check environment")
            print("  python enhanced_test.py errors       # Test error handling")
    else:
        asyncio.run(main())
