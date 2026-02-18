from flask import Flask, render_template, request
from database.db import (
    get_all_distractions,
    get_summary,
    get_category_summary,
    get_daily_summary,
    get_time_slot_summary,
    get_productivity_score
)
from ai.advisor import get_ai_message, respond_to_user_message,generate_analytics_insight

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    records = get_all_distractions()
    total_count, total_duration = get_summary()
    ai_message = get_ai_message(total_duration)

    user_input = ""
    ai_reply = ""

    if request.method == "POST":
        user_input = request.form.get("user_message")
        ai_reply = respond_to_user_message(user_input, total_duration)

    return render_template(
        "index.html",
        records=records,
        total_count=total_count,
        total_duration=total_duration,
        ai_message=ai_message,
        user_input=user_input,
        ai_reply=ai_reply
    )

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


if __name__ == "__main__":
    app.run(debug=True)
