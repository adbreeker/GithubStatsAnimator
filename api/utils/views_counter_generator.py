import os
from .db import get_db_connection, get_or_create_user_views, set_user_views

THEMES = {
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "text_primary": "#24292f",
    },
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "text_primary": "#f0f6fc",
    }
}

async def generate_views_counter_svg(user_agent: str, theme: str, animated: bool = True) -> str:
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
    
    # Modern SVG styling inspired by other generators
    width = len(str(views)) * 22 + 50
    height = 54
    radius = 12
    colors = THEMES[theme]
    shadow = "0 2px 8px rgba(0,0,0,0.10)"
    font_family = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    views_font_size = 28

    views_str = str(views)
    char_count = len(views_str)
    char_width = 22  # spacing per character
    start_x = (width - (char_count * char_width)) / 2 + char_width / 2
    y = height / 2 + 10
    duration = 1.2  # total animation duration per char
    delay_step = 0.25  # delay between each char
    slot_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .counter-bg {{ filter: drop-shadow({shadow}); }}
            .counter-views {{ font-family: {font_family}; font-size: {views_font_size}px; font-weight: bold; fill: {colors['text_primary']}; }}
            .slot-char {{ font-family: {font_family}; font-size: {views_font_size}px; font-weight: bold; fill: {colors['text_primary']}; }}
        </style>
    </defs>
    <rect class="counter-bg" width="{width}" height="{height}" rx="{radius}" fill="{colors['bg']}" stroke="{colors['border']}" stroke-width="2"/>
    '''
    if animated:
        # Slot machine animation using vertical translation of stacked characters
        slot_chars_list = list(slot_chars)
        char_height = views_font_size + 9
        for i, char in enumerate(reversed(views_str)):
            idx = char_count - 1 - i
            x = start_x + idx * char_width
            begin = f'{i * delay_step:.2f}s'
            all_chars = slot_chars_list + [char]
            final_idx = len(all_chars) - 1
            # Group for animation, animate transform on group
            svg += f'<g>'
            svg += f'<animateTransform attributeName="transform" type="translate" '
            svg += f'from="0 0" to="0 {-char_height * final_idx}" dur="{duration}s" begin="{begin}" fill="freeze" />'
            for j, c in enumerate(all_chars):
                y_pos = y + j * char_height
                svg += f'<text x="{x}" y="{y_pos}" text-anchor="middle" class="slot-char">{c}</text>'
            svg += '</g>'
    else:
        # Static centered text
        for i, char in enumerate(views_str):
            x = start_x + i * char_width
            svg += f'<text x="{x}" y="{y}" text-anchor="middle" class="counter-views">{char}</text>'
    svg += '</svg>'
    return svg
