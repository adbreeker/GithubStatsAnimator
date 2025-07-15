import os
from .db import get_db_connection, get_or_create_user_views, set_user_views

def generate_views_counter_svg(user_agent: str) -> str:
    """
    Get or create user in DB (from env), increment views only if user_agent is github-camo, and return SVG with the new value.
    """
    user = os.getenv('GITHUB_USERNAME', 'adbreeker')
    NEON_DATABASE_URL = os.getenv('NEON_DATABASE_URL')

    if NEON_DATABASE_URL:
        db_conn = get_db_connection(NEON_DATABASE_URL)
        try:
            views = get_or_create_user_views(db_conn, user)
            # Only increment if called by GitHub's user agent (github-camo)
            if user_agent.lower().startswith('github-camo'):
                views += 1
                set_user_views(db_conn, user, views)
        except Exception as e:
            print("Database error:", e)
            views = -1
        finally:
            db_conn.close()
    else:
        views = "a crapload"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="40">
  <rect width="180" height="40" rx="8" fill="#222"/>
  <text x="90" y="25" text-anchor="middle" fill="#fff" font-size="24" font-family="'Segoe UI', sans-serif" font-weight="bold">{views}</text>
</svg>'''
