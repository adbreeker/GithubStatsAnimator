"""
Controlled test suite for Account General SVG generation.

Generates 6 SVG files - one for each icon type with specific, controlled configurations
to test all major features and edge cases systematically.

Testing Rules:
- All tests in /tests folder
- All results in /tests/results folder (absolute path)
- 6 SVGs total, one per icon type
- Controlled attributes for comprehensive, predictable coverage
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))
sys.path.insert(0, str(project_root / "api" / "utils"))

from api.utils.account_general_generator import (
    generate_account_general_svg,
    GitHubAccountStatsAPI,
    calculate_basic_stats,
    create_account_general_svg,
    THEMES,
    STAT_CONFIGS,
)

# Absolute path to results directory
RESULTS_DIR = project_root / "tests" / "results"
RESULTS_DIR.mkdir(exist_ok=True)

class AccountGeneralTester:
    def __init__(self):
        # Use environment variable, fallback to 'octocat' only if not found
        self.test_username = os.getenv('GITHUB_USERNAME', 'octocat')
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []
    
    async def test_all_icon_types(self):
        """Generate one SVG for each icon type with specific controlled configurations."""

        # Define specific test configurations for each icon type
        test_configs = [
            {
                'icon': 'user',
                'slots': ['stars', 'commits_total', 'commits_current_year', 'pull_requests', 'code_reviews'],
                'animation_duration': 8
            },
            {
                'icon': 'github',
                'slots': ['issues', 'external_contributions', None, None, None],
                'animation_duration': 8
            },
            {
                'icon': 'streak',
                'slots': [None, None, None, None, None],
                'animation_duration': 8
            },
            {
                'icon': 'user+github',
                'slots': ['stars', None, 'commits_current_year', None, 'issues'],
                'animation_duration': 8  # default
            },
            {
                'icon': 'user+streak',
                'slots': ['code_reviews', None, None, None, 'code_reviews'],
                'animation_duration': 12  # slower
            },
            {
                'icon': 'github+streak',
                'slots': [None, None, 'commits_total', None, None],
                'animation_duration': 2.5  # faster
            }
        ]

        # --- Fetch all data and stats ONCE ---
        needed_stats = set()
        for config in test_configs:
            for slot in config['slots']:
                if slot:
                    needed_stats.add(slot)
            if 'streak' in config['icon'] or '+streak' in config['icon']:
                needed_stats.add('streak')
        api = GitHubAccountStatsAPI()
        user_data = await api.fetch_account_stats(self.test_username, needed_stats)
        stats = calculate_basic_stats(user_data)
        # Print all stats including account creation year
        print("\n--- Account General Stats for:", self.test_username, "---")
        print("Account creation date:", user_data.get('createdAt', 'N/A'))
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("---------------------------------------------\n")

        # --- Generate SVGs using cached data ---
        from api.utils.account_general_generator import generate_icon_svg, create_rotating_icon_svg
        width, height = 400, 200
        padding = 20
        title_height = 35
        title_x = padding + 10
        stats_x = padding + 10
        stats_start_y = title_height + 20
        stats_spacing = 25
        icon_size = 80
        icon_x = width - icon_size - padding - 10
        third_row_y = stats_start_y + (2 * stats_spacing)
        icon_y = third_row_y - (icon_size // 2) + 5
        avatar_url = user_data.get('avatarUrl')
        streak_value = stats.get('streak', 0)

        for i, config in enumerate(test_configs):
            try:
                icon = config['icon']
                slots = config['slots']
                animation_duration = config['animation_duration']
                theme = 'dark' if i % 2 == 0 else 'light'
                colors = THEMES[theme]
                # Ensure exactly 5 slots
                slots = (slots + [None]*5)[:5]
                # Prepare stat items
                stat_items = []
                stats_width = width - stats_x - icon_size - padding
                for idx, slot in enumerate(slots):
                    if slot is None:
                        continue
                    value = stats.get(slot, 0)
                    label = STAT_CONFIGS.get(slot, {}).get('label', slot.replace('_', ' ').title())
                    from api.utils.account_general_generator import format_number, create_stat_item_svg
                    formatted_value = format_number(value)
                    x = stats_x
                    y = stats_start_y + (idx * stats_spacing)
                    stat_items.append(create_stat_item_svg(label, formatted_value, slot, x, y, theme, stats_width))
                # Icon SVG
                if '+' in icon:
                    icon1, icon2 = icon.split('+')
                    icon_svg = await create_rotating_icon_svg(
                        icon1, icon2, self.test_username, theme, icon_x, icon_y, avatar_url, icon_size, streak_value, animation_duration)
                else:
                    icon_svg = await generate_icon_svg(
                        icon, self.test_username, theme, icon_x, icon_y, avatar_url, icon_size, streak_value)
                svg_content = create_account_general_svg(
                    self.test_username, user_data, icon_svg, stat_items, title_x, colors)
                filename = f"account_general_{i+1}_{icon.replace('+', '_')}_{self.timestamp}.svg"
                filepath = RESULTS_DIR / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                clean_slots = [slot for slot in slots if slot is not None]
                self.results.append({
                    'test': f'Icon Type {i+1}: {icon}',
                    'status': 'PASS',
                    'file': filename,
                    'icon': icon,
                    'theme': theme,
                    'slots': clean_slots,
                    'slot_count': len(clean_slots),
                    'size': len(svg_content),
                    'animation_duration': animation_duration,
                    'config_id': i + 1
                })
                print(f"✅ Generated {i+1}/6: {filename}")
                print(f"   Theme: {theme}, Slots: {len(clean_slots)} ({', '.join(clean_slots) if clean_slots else 'none'})")
                if '+' in icon:
                    print(f"   Animation Duration: {animation_duration}s")
            except Exception as e:
                icon_name = config.get('icon', 'unknown')
                self.results.append({
                    'test': f'Icon Type {i+1}: {icon_name}',
                    'status': 'FAIL',
                    'icon': icon_name,
                    'error': str(e),
                    'theme': 'N/A',
                    'slots': [],
                    'slot_count': 0,
                    'animation_duration': 'N/A',
                    'config_id': i + 1
                })
                print(f"❌ Failed {i+1}/6: {icon_name} - {e}")
    
    async def run_all_tests(self):
        """Run the controlled test suite."""
        print(f"🚀 Starting Account General SVG Tests (6 controlled configurations)")
        print(f"📁 Results will be saved to: {RESULTS_DIR}")
        print(f"📅 Timestamp: {self.timestamp}")
        print("-" * 60)
        
        await self.test_all_icon_types()
        
        # Generate test report
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive test report."""
        report_filename = f"test_report_account_general_{self.timestamp}.md"
        report_path = RESULTS_DIR / report_filename
        
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        total = len(self.results)
        
        report_content = f"""# Account General SVG Test Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Test Username:** {self.test_username}
**Test Strategy:** 6 SVGs with controlled, specific configurations

## Test Configurations

1. **user** - Full stats (5 slots): stars, commits_total, commits_year, pull_requests, code_reviews
2. **github** - Partial stats (2 slots): issues, external_contributions
3. **streak** - No stats (0 slots): icon only
4. **user+github** - Selective stats (3 slots): stars, commits_year, issues [8s animation]
5. **user+streak** - Duplicate slots (2 slots): code_reviews (x2) [12s animation]
6. **github+streak** - Single stat (1 slot): commits_total [2.5s animation]

## Summary
- **Total Tests:** {total}
- **Passed:** {passed} ✅
- **Failed:** {failed} ❌
- **Success Rate:** {(passed/total*100):.1f}%

## Test Results

"""
        
        for i, result in enumerate(self.results, 1):
            status_emoji = "✅" if result['status'] == 'PASS' else "❌"
            report_content += f"### {status_emoji} Test {result.get('config_id', i)}: {result['icon']}\n"
            
            if result['status'] == 'PASS':
                report_content += f"- **File:** `{result['file']}`\n"
                report_content += f"- **Theme:** {result['theme']}\n"
                slots_str = ', '.join(str(slot) for slot in result['slots'] if slot is not None)
                report_content += f"- **Slots:** {result['slot_count']} slots ({slots_str if slots_str else 'none'})\n"
                report_content += f"- **Size:** {result['size']} bytes\n"
                if '+' in result['icon']:
                    report_content += f"- **Animation Duration:** {result['animation_duration']}s\n"
            else:
                report_content += f"- **Error:** {result['error']}\n"
            
            report_content += "\n"
        
        report_content += f"""
## Coverage Analysis

**Icon Types Tested:** {len([r for r in self.results if r['status'] == 'PASS'])}/6
- Basic Icons: {len([r for r in self.results if r['status'] == 'PASS' and '+' not in r['icon']])} (user, github, streak)
- Rotating Icons: {len([r for r in self.results if r['status'] == 'PASS' and '+' in r['icon']])} (user+github, user+streak, github+streak)

**Themes Tested:** {len(set(r['theme'] for r in self.results if r['status'] == 'PASS'))} (alternating dark/light)
**Animation Durations:** 3 different speeds (8s, 12s, 2.5s)
**Slot Configurations:** 6 different patterns (0-5 slots, including duplicates and None values)

## Files Generated

All SVG files saved to: `{RESULTS_DIR}`

**Quick Test:** Open any SVG file in a browser to verify:
- Visual appearance and layout
- Animation timing for rotating icons:
  - user+github: 8s (default)
  - user+streak: 12s (slower)
  - github+streak: 2.5s (faster)
- Theme colors and styling
- Slot content and positioning
- Edge cases: empty slots, duplicate slots, varying slot counts
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print("-" * 60)
        print(f"📊 Test Report: {report_filename}")
        print(f"📈 Results: {passed}/{total} tests passed")
        
        if failed > 0:
            print(f"⚠️  {failed} tests failed")
        else:
            print("🎉 All tests passed!")
        
        print(f"📁 {passed} SVG files generated for visual verification")

async def main():
    """Main test execution function."""
    print("🧪 GitHub Stats Animator - Account General SVG Test Suite (Controlled)")
    print("=" * 70)
    
    # Check environment variables
    github_username = os.getenv('GITHUB_USERNAME')
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠️  GITHUB_TOKEN not found in environment variables")
        print("   Tests will run but may not fetch real data")
    
    if not github_username:
        print("⚠️  GITHUB_USERNAME not found in environment variables")
        print("   Using fallback username 'octocat'")
        print(f"📝 Test Username: octocat (fallback)")
    else:
        print(f"📝 Test Username: {github_username} (from environment)")
    
    print("� Controlled Test Configurations:")
    print("   1. user: 5 slots (full stats)")
    print("   2. github: 2 slots (partial)")
    print("   3. streak: 0 slots (icon only)")
    print("   4. user+github: 3 slots [8s animation]")
    print("   5. user+streak: 2 slots (duplicate) [12s animation]")
    print("   6. github+streak: 1 slot [2.5s animation]")
    print()
    
    tester = AccountGeneralTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
