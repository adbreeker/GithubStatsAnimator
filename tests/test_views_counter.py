"""
Controlled test for Views Counter SVG generation.

- Generates 1 SVG file using the views counter generator
- Follows project testing rules: all results in /tests/results (absolute path)
- Logs output and saves SVG for visual verification
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Add the project root and api/utils to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))
sys.path.insert(0, str(project_root / "api" / "utils"))

from api.utils.views_counter_generator import generate_views_counter_svg

# Absolute path to results directory
RESULTS_DIR = project_root / "tests" / "results"
RESULTS_DIR.mkdir(exist_ok=True)

async def test_views_counter():
    """
    Generate one SVG for the views counter and save results.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Animated SVG
    svg_animated = await generate_views_counter_svg(user_agent='null', theme='dark', animated=True)
    filename_animated = f"views_counter_animated_{timestamp}.svg"
    filepath_animated = RESULTS_DIR / filename_animated
    with open(filepath_animated, 'w', encoding='utf-8') as f:
        f.write(svg_animated)

    # Static SVG
    svg_static = await generate_views_counter_svg(user_agent='null', theme='light', animated=False)
    filename_static = f"views_counter_static_{timestamp}.svg"
    filepath_static = RESULTS_DIR / filename_static
    with open(filepath_static, 'w', encoding='utf-8') as f:
        f.write(svg_static)

    print(f"✅ Views counter SVGs generated: {filename_animated}, {filename_static}")

if __name__ == "__main__":
    asyncio.run(test_views_counter())
