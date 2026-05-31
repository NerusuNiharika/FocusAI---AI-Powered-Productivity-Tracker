import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("distraction.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM distraction_log")

apps = {
    "Entertainment": ["YouTube", "Netflix", "Spotify Free"],
    "Social Media": ["Instagram", "Twitter"],
    "Browsing": ["Chrome News", "Random Blog","Linkedln"],
    "Other": ["Unknown App"]
}

start_date = datetime.now() - timedelta(days=30)

for day in range(30):
    current_day = start_date + timedelta(days=day)

    for _ in range(random.randint(5, 10)):

        category = random.choice(list(apps.keys()))
        app_name = random.choice(apps[category])

        duration = random.randint(5, 60)

        hour = random.choice([9, 12, 15, 18, 21])
        minute = random.randint(0, 59)

        timestamp = current_day.replace(hour=hour, minute=minute)

        cursor.execute("""
            INSERT INTO distraction_log (app_name, category, duration, datetime)
            VALUES (?, ?, ?, ?)
        """, (app_name, category, duration, timestamp.strftime("%Y-%m-%d %H:%M:%S")))

conn.commit()
conn.close()

print("Clean distraction dataset inserted!")