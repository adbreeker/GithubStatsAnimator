#!/usr/bin/env python3
"""
Quick test for the final improvements
"""
import asyncio
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.top_languages_generator import create_language_bar_chart

def test_final_improvements():
    """Test the final improvements: start-from-zero animation and winner styling"""
    print("🎯 Testing final improvements...")
    
    # Set up results directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    test_languages = [
        ("JavaScript", 45.2, "#f1e05a"),
        ("Python", 23.8, "#3572a5"), 
        ("TypeScript", 15.1, "#2b7489"),
        ("C", 10.3, "#555555"),
        ("Other", 5.6, "#858585")
    ]
    
    # Test default size
    svg_content = create_language_bar_chart(test_languages, "dark", 400, 300, 1)
    
    output_file = os.path.join(results_dir, "final_improvements.svg")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✅ SVG generated: {output_file}")
    
    # Check improvements
    improvements = []
    
    # Check for start-from-zero animation
    if "transform: scaleX(0);" in svg_content:
        improvements.append("✅ Bars start from zero (no flash)")
    else:
        improvements.append("❌ Bars don't start from zero")
    
    # Check for winner emoji and outline
    if "🏆" in svg_content:
        improvements.append("✅ Winner emoji present")
    else:
        improvements.append("❌ Winner emoji missing")
        
    if 'stroke="#0d1117"' in svg_content or 'stroke="#ffffff"' in svg_content:
        improvements.append("✅ Text outline present")
    else:
        improvements.append("❌ Text outline missing")
        
    if 'font-weight="600"' in svg_content:
        improvements.append("✅ Top language bold styling")
    else:
        improvements.append("❌ Top language not bold")
    
    print("\n🔍 Final improvements status:")
    for improvement in improvements:
        print(f"   {improvement}")
    
    # Test different themes
    print("\n🎨 Testing light theme...")
    svg_light = create_language_bar_chart(test_languages, "light", 400, 300, 1)
    light_output_file = os.path.join(results_dir, "final_improvements_light.svg")
    with open(light_output_file, "w", encoding="utf-8") as f:
        f.write(svg_light)
    
    if "🏆" in svg_light and "transform: scaleX(0);" in svg_light:
        print("   ✅ Light theme works correctly")
    else:
        print("   ❌ Light theme issues")
    
    return svg_content

if __name__ == "__main__":
    test_final_improvements()
    print("\n" + "="*50)
    print("🎉 Final improvements testing complete!")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    print(f"📁 Check {results_dir} for output files")
    print("🌐 Open in browser to see animations")
