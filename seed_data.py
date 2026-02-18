import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("distraction.db")
cursor = conn.cursor()

# Clear old data (optional but recommended)
cursor.execute("DELETE FROM distraction_log")

apps = {
    "Work": ["VS Code", "Slack", "Chrome Docs", "Terminal"],
    "Entertainment": ["YouTube", "Netflix", "Spotify"],
    "Social Media": ["Instagram", "Twitter", "LinkedIn"]
}

start_date = datetime.now() - timedelta(days=30)

for day in range(30):
    current_day = start_date + timedelta(days=day)

    # 8–12 entries per day
    for _ in range(random.randint(8, 12)):

        # Simulate realistic category distribution
        category = random.choices(
            ["Work", "Entertainment", "Social Media"],
            weights=[50, 30, 20]
        )[0]

        app_name = random.choice(apps[category])

        # Simulate realistic durations
        if category == "Work":
            duration = random.randint(20, 90)
        elif category == "Entertainment":
            duration = random.randint(15, 60)
        else:
            duration = random.randint(5, 40)

        # Simulate time slots
        hour = random.choices(
            [9, 11, 14, 16, 19, 21],
            weights=[20, 20, 25, 15, 15, 5]
        )[0]

        minute = random.randint(0, 59)

        timestamp = current_day.replace(hour=hour, minute=minute)

        cursor.execute("""
            INSERT INTO distraction_log (app_name, category, duration, datetime)
            VALUES (?, ?, ?, ?)
        """, (app_name, category, duration, timestamp.strftime("%Y-%m-%d %H:%M:%S")))

conn.commit()
conn.close()

print("Professional medium dataset inserted successfully!")
