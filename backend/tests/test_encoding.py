"""
Test encoding and special characters handling
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.top_languages_generator import create_language_bar_chart

def test_encoding():
    """Test various special characters and encoding"""
    print("🔤 Testing encoding and special characters...")
    
    # Test languages with special characters
    test_languages = [
        ("C#", 45.0),
        ("C++", 25.0), 
        ("F#", 15.0),
        ("Objective-C", 10.0),
        ("Shell & Scripts", 5.0)
    ]
    
    # Test with different sizes
    test_cases = [
        {"width": 400, "height": 300, "theme": "dark", "name": "normal"},
        {"width": 250, "height": 200, "theme": "light", "name": "small"},
        {"width": 800, "height": 400, "theme": "dark", "name": "large"}
    ]
    
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    for case in test_cases:
        print(f"\n📏 Testing {case['name']} size ({case['width']}x{case['height']})...")
        
        try:
            svg = create_language_bar_chart(
                languages=test_languages,
                theme=case['theme'],
                width=case['width'],
                height=case['height'],
                decimal_places=1
            )
            
            # Check for encoding issues
            if "�" in svg:
                print(f"   ❌ Encoding issue detected!")
            else:
                print(f"   ✅ No encoding issues found")
            
            # Check for proper XML escaping
            if "&amp;" in svg or "&lt;" in svg or "&gt;" in svg:
                print(f"   ✅ XML escaping working")
            
            # Save the test file
            filename = os.path.join(results_dir, f"encoding_test_{case['name']}.svg")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg)
            
            print(f"   📄 Saved: encoding_test_{case['name']}.svg ({len(svg)} chars)")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎯 Encoding tests complete!")

if __name__ == "__main__":
    test_encoding()
