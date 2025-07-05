#!/usr/bin/env python3
"""
Test the animated percentages and language name display
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.top_languages_generator import create_language_bar_chart

def test_animated_percentages_and_names():
    """Test the SVG generation with animated percentages and full language names"""
    print("Testing animated percentages and language name display...")
    
    # Test data with some longer language names
    test_languages = [
        ("JavaScript", 45.2, "#f1e05a"),
        ("Python", 23.8, "#3572a5"),
        ("TypeScript", 15.1, "#2b7489"),
        ("Jupyter Notebook", 10.3, "#da5b0b"),  # Longer name to test layout
        ("Other", 5.6, "#858585")
    ]
    
    # Test with default dimensions
    svg_content = create_language_bar_chart(test_languages, "dark", 400, 300, 1)
    
    # Save to results folder - always use absolute path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    output_file = os.path.join(results_dir, "test_animated_percentages.svg")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print("✓ SVG generated successfully")
    print(f"✓ File saved as '{output_file}'")
    
    # Check for key features
    features = []
    
    if 'class="bar"' in svg_content:
        features.append("✓ Bar animations present")
    else:
        features.append("✗ Bar animations missing")
        
    if 'class="text"' in svg_content:
        features.append("✓ Text animations present")
    else:
        features.append("✗ Text animations missing")
        
    if 'animation-delay:' in svg_content:
        features.append("✓ Staggered delays present")
    else:
        features.append("✗ Staggered delays missing")
        
    if 'fadeInText' in svg_content:
        features.append("✓ Text fade animation present")
    else:
        features.append("✗ Text fade animation missing")
    
    # Check that no language names are truncated
    if "…" in svg_content or "..." in svg_content:
        features.append("✗ Language names are truncated")
    else:
        features.append("✓ No language name truncation")
        
    # Check that all language names are present
    all_names_present = all(lang[0] in svg_content for lang in test_languages)
    if all_names_present:
        features.append("✓ All language names present")
    else:
        features.append("✗ Some language names missing")
    
    print("\nFeatures status:")
    for feature in features:
        print(f"  {feature}")
    
    # Count animation delays
    delay_count = svg_content.count('animation-delay:')
    expected_animations = len(test_languages) * 2  # bars + text
    print(f"\nAnimated elements: {delay_count}/{expected_animations}")
    
    # Test with different sizes to ensure layout works
    print("\nTesting different sizes...")
    
    sizes_to_test = [
        (300, 200, "small"),
        (500, 350, "medium"), 
        (600, 400, "large"),
        (450, 250, "wide")
    ]
    
    for width, height, size_name in sizes_to_test:
        svg_content = create_language_bar_chart(test_languages, "dark", width, height, 1)
        filename = os.path.join(results_dir, f"test_animated_{size_name}.svg")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        # Check for truncation in this size
        has_truncation = "…" in svg_content or "..." in svg_content
        status = "✗ TRUNCATED" if has_truncation else "✓ No truncation"
        print(f"  {size_name} ({width}x{height}): {status}")
    
    return svg_content

def test_with_real_api():
    """Test with actual GitHub API"""
    print("\nTesting with real API...")
    
    try:
        from utils.top_languages_generator import create_top_languages_svg
        
        async def run_api_test():
            # Test with a known user
            username = "torvalds"
            
            svg_content = await create_top_languages_svg(
                username=username,
                theme="dark",
                languages_count=6,
                decimal_places=1,
                width=450,
                height=350
            )
            
            # Save result - always use absolute path relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            results_dir = os.path.join(script_dir, "results")
            os.makedirs(results_dir, exist_ok=True)
            
            output_file = os.path.join(results_dir, "test_real_api_animated.svg")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            print(f"✓ Real API test completed for user: {username}")
            print(f"✓ File saved as '{output_file}'")
            
            # Check for issues
            issues = []
            
            if "Error generating" in svg_content:
                issues.append("✗ Error in SVG generation")
            elif "Token Error" in svg_content:
                issues.append("⚠ GitHub token error")
            else:
                issues.append("✓ SVG generated successfully")
                
            if 'class="bar"' in svg_content:
                issues.append("✓ Bar animations present")
            else:
                issues.append("✗ Bar animations missing")
                
            if "…" in svg_content or "..." in svg_content:
                issues.append("✗ Language names truncated")
            else:
                issues.append("✓ No truncation in real data")
            
            print("\nReal API test results:")
            for issue in issues:
                print(f"  {issue}")
                
            return svg_content
        
        return asyncio.run(run_api_test())
        
    except Exception as e:
        print(f"✗ Real API test failed: {e}")
        return None

if __name__ == "__main__":
    # Run tests
    test_animated_percentages_and_names()
    test_with_real_api()
    
    print("\n" + "="*50)
    print("✅ All tests completed!")
    print("📁 Results saved in tests/results/ folder")
    print("🌐 Open the SVG files in a browser to see animations")
