from flask import Flask, render_template, request
import threading

from database.db import (
    get_all_distractions,
    get_summary,
    get_category_summary,
    get_daily_summary,
    get_time_slot_summary,
    get_productivity_score,
    create_table
)

from ai.advisor import (
    get_ai_message,
    respond_to_user_message,
    generate_analytics_insight
)

from tracker.window_tracker import (
    start_tracking,
    stop_tracking
)


app = Flask(__name__)

# Create database tables when the application starts.
# This works both locally and when Gunicorn starts the app on Render.
create_table()

# Global tracker thread reference
tracker_thread = None


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    global tracker_thread

    # Check current tracker state
    tracking_status = (
        "Started"
        if tracker_thread and tracker_thread.is_alive()
        else "Stopped"
    )

    if request.method == "POST":

        action = request.form.get("action")

        # ----------------------------------------------------
        # START TRACKING
        # ----------------------------------------------------

        if action == "start":

            if tracker_thread is None or not tracker_thread.is_alive():

                tracker_thread = threading.Thread(
                    target=start_tracking,
                    daemon=True
                )

                tracker_thread.start()

                tracking_status = "Started"

        # ----------------------------------------------------
        # STOP TRACKING
        # ----------------------------------------------------

        elif action == "stop":

            stop_tracking()

            tracking_status = "Stopped"

    return render_template(
        "home.html",
        tracking_status=tracking_status
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    records = get_all_distractions()

    total_count, total_duration = get_summary()

    ai_message = get_ai_message(total_duration)

    user_input = ""
    ai_reply = ""

    if request.method == "POST":

        user_input = request.form.get("user_message", "")

        ai_reply = respond_to_user_message(
            user_input,
            total_duration
        )

    return render_template(
        "index.html",
        records=records,
        total_count=total_count,
        total_duration=total_duration,
        ai_message=ai_message,
        user_input=user_input,
        ai_reply=ai_reply
    )


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
def analytics():

    category_data = get_category_summary()

    daily_data = get_daily_summary()

    time_slot_data = get_time_slot_summary()

    productivity_data = get_productivity_score()

    has_data = bool(category_data)

    insights = generate_analytics_insight(
        category_data,
        time_slot_data,
        productivity_data,
        daily_data
    )

    return render_template(
        "analytics.html",
        category_data=category_data,
        daily_data=daily_data,
        time_slot_data=time_slot_data,
        productivity_data=productivity_data,
        insights=insights,
        has_data=has_data
    )


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)