"""
Controlled test for Views Counter SVG generation.

- Generates 1 SVG file using the views counter generator
- Follows project testing rules: all results in /tests/results (absolute path)
- Logs output and saves SVG for visual verification
"""

import os
import sys
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

def test_views_counter():
    """
    Generate one SVG for the views counter and save results.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    svg_content = generate_views_counter_svg(user_agent='null')
    filename = f"views_counter_{timestamp}.svg"
    filepath = RESULTS_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print(f"✅ Views counter SVG generated: {filename}")

if __name__ == "__main__":
    test_views_counter()
