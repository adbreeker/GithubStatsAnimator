import random

def generate_views_counter_svg(counter_value: int = None) -> str:
    """
    Generate a simple SVG with a random or provided counter value.
    """
    if counter_value is None:
        counter_value = random.randint(1000, 99999)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="40">
  <rect width="180" height="40" rx="8" fill="#222"/>
  <text x="90" y="25" text-anchor="middle" fill="#fff" font-size="24" font-family="'Segoe UI', sans-serif" font-weight="bold">{counter_value}</text>
</svg>'''
