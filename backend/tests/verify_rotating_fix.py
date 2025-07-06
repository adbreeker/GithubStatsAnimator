"""
Simple verification test for the rotating icon pre-flip fix
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.account_general_generator import create_account_general_svg

async def verify_rotating_fix():
    """Quick test to verify the rotating icon has pre-flipped second side"""
    
    print("🔄 Verifying rotating icon pre-flip implementation...")
    
    # Generate SVG with rotating icon
    svg_content = await create_account_general_svg(
        username="octocat",
        icon="github+user",  # This should create rotating icon
        theme="dark",
        slots=['stars', 'commits_year', 'pull_requests', 'issues', None]
    )
    
    # Check for the specific pre-flip transform
    expected_transform = 'transform="scaleX(-1) translate(-80, 0)"'
    
    if expected_transform in svg_content:
        print("✅ SUCCESS: Pre-flip transform found in SVG")
        print(f"   Transform: {expected_transform}")
    else:
        print("❌ FAILED: Pre-flip transform not found")
        return False
    
    # Check for coin animation CSS
    animation_checks = [
        'animation: coinFlip 8s infinite ease-in-out',
        'animation: showSide1 8s infinite ease-in-out',
        'animation: showSide2 8s infinite ease-in-out',
        'transform: rotateY(180deg)'
    ]
    
    for check in animation_checks:
        if check in svg_content:
            print(f"✅ Found: {check}")
        else:
            print(f"❌ Missing: {check}")
            return False
    
    print("\n🎉 All checks passed! The rotating icon fix is properly implemented.")
    print("📝 The second side of the rotating logo is pre-flipped using scaleX(-1)")
    print("🔄 This ensures both sides appear correctly during the coin-flip animation")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(verify_rotating_fix())
    if success:
        print("\n✨ Rotating icon fix verification: COMPLETE")
    else:
        print("\n💥 Rotating icon fix verification: FAILED")
