import time
import pygetwindow as gw
from datetime import datetime
from database.db import insert_distraction, get_category

# Global control flag
tracking = False


# ---------------- GET ACTIVE WINDOW ----------------
def get_active_window():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown"
    except:
        return "Unknown"


# ---------------- TRACK USAGE ----------------
def track_usage():
    global tracking

    last_window = None
    start_time = datetime.now()

    while tracking:
        current_window = get_active_window()

        # If window changed → save previous
        if current_window != last_window:
            end_time = datetime.now()

            if last_window is not None:
                duration = int((end_time - start_time).total_seconds())

                if duration > 2:  # avoid noise
                    category = get_category(last_window)
                    print("Saving:", last_window, category, duration)
                    insert_distraction(last_window, category, duration)

            # Reset tracking for new window
            last_window = current_window
            start_time = datetime.now()

        time.sleep(2)

    # 🔥 SAVE LAST WINDOW WHEN STOPPING
    if last_window is not None:
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds())

        if duration > 2:
            category = get_category(last_window)
            print("Final Save:", last_window, category, duration)
            insert_distraction(last_window, category, duration)


# ---------------- START TRACKING ----------------
def start_tracking():
    global tracking

    if tracking:
        print("Already tracking...")
        return

    tracking = True
    print("Tracking started...")

    track_usage()   # runs inside thread


# ---------------- STOP TRACKING ----------------
def stop_tracking():
    global tracking

    if not tracking:
        print("Tracking already stopped...")
        return

    tracking = False
    print("Tracking stopping...")