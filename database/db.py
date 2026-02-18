import sqlite3

DATABASE_NAME = "distraction.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_NAME)


def get_all_distractions():
    """
    Fetches all distraction records from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name, category, duration
    FROM distraction_log
    ORDER BY datetime DESC
    LIMIT 10
""")


    data = cursor.fetchall()
    conn.close()

    return data
def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), SUM(duration)
        FROM distraction_log
    """)

    result = cursor.fetchone()
    conn.close()

    total_distractions = result[0]
    total_duration = result[1] if result[1] else 0

    return total_distractions, total_duration

def get_category_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(duration)
        FROM distraction_log
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    return data
def get_daily_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DATE(datetime), SUM(duration)
        FROM distraction_log
        GROUP BY DATE(datetime)
        ORDER BY DATE(datetime)
    """)
    data = cursor.fetchall()
    conn.close()
    return data 
def get_time_slot_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE
                WHEN CAST(strftime('%H', datetime) AS INTEGER) BETWEEN 6 AND 11 THEN 'Morning'
                WHEN CAST(strftime('%H', datetime) AS INTEGER) BETWEEN 12 AND 16 THEN 'Afternoon'
                WHEN CAST(strftime('%H', datetime) AS INTEGER) BETWEEN 17 AND 21 THEN 'Evening'
                ELSE 'Night'
            END AS time_slot,
            SUM(duration)
        FROM distraction_log
        WHERE datetime IS NOT NULL
        GROUP BY time_slot
    """)

    data = cursor.fetchall()
    conn.close()

    return data

def get_productivity_score():
    daily_data = get_daily_summary()

    scores = []
    for date, duration in daily_data:
        score = max(0, 100 - duration)
        scores.append((date, score))

    return scores

