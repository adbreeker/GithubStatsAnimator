import os
import psycopg2

# Get Neon database connection URL from environment variable
NEON_DATABASE_URL = os.getenv('NEON_DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(NEON_DATABASE_URL, sslmode='require')

def get_or_create_user_views(db_conn, user: str) -> int:
    """
    Get the current views for a user, or create the user with 0 views if not exists.
    Returns the current views count.
    """
    try:
        with db_conn:
            with db_conn.cursor() as cur:
                cur.execute("SELECT views FROM \"GithubStatsAnimator\" WHERE \"user\" = %s", (user,))
                row = cur.fetchone()
                if row:
                    return row[0]
                # Create user with 0 views
                cur.execute("INSERT INTO \"GithubStatsAnimator\" (\"user\", views) VALUES (%s, 0)", (user,))
                return 0
    except Exception as e:
        print(f"Error getting or creating user views: {e}")
        raise

def set_user_views(db_conn, user: str, views: int) -> int:
    """
    Set the views for a user and return the new value.
    """
    try:
        with db_conn:
            with db_conn.cursor() as cur:
                cur.execute("UPDATE \"GithubStatsAnimator\" SET views = %s WHERE \"user\" = %s RETURNING views", (views, user))
    except Exception as e:
        print(f"Error setting user views: {e}")
        raise
