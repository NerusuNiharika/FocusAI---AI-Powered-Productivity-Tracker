import sqlite3

DATABASE_NAME = "distraction.db"

# Productive categories
PRODUCTIVE_CATEGORIES = ["Work", "Development", "Study"]


# ---------------- CONNECTION ----------------
def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ---------------- CREATE TABLE ----------------
def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS distraction_log (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            app_name TEXT,

            category TEXT,

            duration INTEGER,

            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()


# ---------------- INSERT DATA ----------------
def insert_distraction(app_name, category, duration):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO distraction_log (
            app_name,
            category,
            duration
        )
        VALUES (?, ?, ?)
    """, (app_name, category, duration))

    conn.commit()

    conn.close()


# ---------------- CATEGORY LOGIC ----------------
def get_category(app_name):

    app_name = app_name.lower()

    # ---------------- IGNORE OWN PROJECT ----------------
    ignore_keywords = [
        "focusai",
        "distraction detection",
        "werkzeug",
        "localhost",
        "127.0.0.1",
        "google ai studio",
        "api keys"
    ]

    if any(keyword in app_name for keyword in ignore_keywords):

        return "Development"

    # ---------------- ENTERTAINMENT ----------------
    elif any(keyword in app_name for keyword in [
        "youtube",
        "netflix",
        "spotify"
    ]):

        return "Entertainment"

    # ---------------- SOCIAL MEDIA ----------------
    elif any(keyword in app_name for keyword in [
        "instagram",
        "facebook",
        "twitter",
        "linkedin",
        "whatsapp"
    ]):

        return "Social Media"

    # ---------------- DEVELOPMENT ----------------
    elif any(keyword in app_name for keyword in [
        "visual studio code",
        "pycharm",
        "terminal",
        "leetcode",
        "github",
        "stack overflow",
        "jupyter",
        "indiabix",
        "codechef",
        "geeksforgeeks"
    ]):

        return "Development"

    # ---------------- WORK ----------------
    elif any(keyword in app_name for keyword in [
        "word",
        "excel",
        "powerpoint",
        "docs",
        "notion"
    ]):

        return "Work"

    # ---------------- BROWSING ----------------
    elif "chrome" in app_name or "edge" in app_name:

        return "Browsing"

    # ---------------- OTHER ----------------
    else:

        return "Other"


# ---------------- FETCH RECENT RECORDS ----------------
def get_all_distractions():

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


# ---------------- SUMMARY ----------------
def get_summary():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), SUM(duration)
        FROM distraction_log
        WHERE category NOT IN ('Development', 'Work')
    """)

    result = cursor.fetchone()

    conn.close()

    total_distractions = result[0]

    total_duration = result[1] if result[1] else 0

    return total_distractions, total_duration


# ---------------- CATEGORY SUMMARY ----------------
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

    order = [
        "Social Media",
        "Entertainment",
        "Browsing",
        "Development",
        "Work",
        "Other"
    ]

    data.sort(
        key=lambda x: order.index(x[0]) if x[0] in order else 999
    )

    return data


# ---------------- DAILY SUMMARY ----------------
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


# ---------------- TIME SLOT SUMMARY ----------------
def get_time_slot_summary():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE

                WHEN CAST(strftime('%H', datetime) AS INTEGER)
                    BETWEEN 5 AND 11
                THEN 'Morning'

                WHEN CAST(strftime('%H', datetime) AS INTEGER)
                    BETWEEN 12 AND 16
                THEN 'Afternoon'

                WHEN CAST(strftime('%H', datetime) AS INTEGER)
                    BETWEEN 17 AND 20
                THEN 'Evening'

                ELSE 'Late Night'

            END AS time_slot,

            SUM(duration)

        FROM distraction_log

        WHERE datetime IS NOT NULL

        GROUP BY time_slot
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- PRODUCTIVITY SCORE ----------------
def get_productivity_score():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            DATE(datetime),

            SUM(
                CASE
                    WHEN category IN ('Development', 'Work')
                    THEN duration
                    ELSE 0
                END
            ) AS productive_time,

            SUM(
                CASE
                    WHEN category NOT IN ('Development', 'Work')
                    THEN duration
                    ELSE 0
                END
            ) AS distraction_time

        FROM distraction_log

        GROUP BY DATE(datetime)

        ORDER BY DATE(datetime)
    """)

    rows = cursor.fetchall()

    conn.close()

    scores = []

    for row in rows:

        date = row[0]

        productive_time = row[1] if row[1] else 0

        distraction_time = row[2] if row[2] else 0

        total_time = productive_time + distraction_time

        if total_time == 0:

            score = 0

        else:

            score = round(
                (productive_time / total_time) * 100,
                2
            )

        scores.append((date, score))

    return scores