def get_ai_message(total_duration):
    """
    AI summary based on total distraction time.
    """

    if total_duration >= 120:
        return "🚨 High distraction detected today. Strongly consider restructuring your schedule."
    elif total_duration >= 60:
        return "⚠️ You were distracted quite a bit today. Try using focused work sessions."
    elif total_duration >= 30:
        return "🙂 Moderate distractions today. You're improving — keep going."
    else:
        return "✅ Excellent focus today! Keep maintaining this routine."


def respond_to_user_message(user_message, total_duration):
    """
    Context-aware AI response using both:
    - User message
    - Productivity data
    """

    message = user_message.lower()

    # Emotional state detection
    if "tired" in message or "exhausted" in message:
        if total_duration > 60:
            return "😴 You seem tired and had many distractions. A proper break would really help."
        else:
            return "😴 Feeling tired is okay. Short breaks can boost focus."

    if "can't focus" in message or "distracted" in message:
        if total_duration > 60:
            return "🧠 Focus has been difficult today. Try a 25-minute deep focus session."
        else:
            return "🧠 You're doing better than you think. Reduce notifications and try again."

    if "happy" in message or "good" in message:
        if total_duration < 30:
            return "🎉 Great mood and great focus — that's a powerful combo!"
        else:
            return "🙂 Glad you're feeling good. Let’s channel that energy productively."

    # Default response
    return "💡 Thanks for sharing. Small consistent improvements make a big difference."

def generate_analytics_insight(category_data, time_slot_data, productivity_data, daily_data):
    insights = []

    # 1️⃣ Highest distraction category
    if category_data:
        highest_category = max(category_data, key=lambda x: x[1])
        insights.append(
            f"Your biggest source of distraction is {highest_category[0]}."
        )

    # 2️⃣ Most distracting time slot
    if time_slot_data:
        worst_time = max(time_slot_data, key=lambda x: x[1])
        insights.append(
            f"You tend to get distracted most during the {worst_time[0]}."
        )

    # 3️⃣ Daily distraction trend (NEW)
    if daily_data and len(daily_data) >= 2:
        first_day = daily_data[0][1]
        last_day = daily_data[-1][1]

        if last_day > first_day:
            insights.append("Your daily distraction time has increased over the period.")
        elif last_day < first_day:
            insights.append("Your daily distraction time has decreased recently, which is a positive sign.")
        else:
            insights.append("Your daily distraction time has remained consistent.")

    # 4️⃣ Productivity trend
    if productivity_data and len(productivity_data) >= 2:
        first_score = productivity_data[0][1]
        last_score = productivity_data[-1][1]

        if last_score > first_score:
            insights.append("Your productivity trend is improving over time.")
        elif last_score < first_score:
            insights.append("Your productivity has slightly declined recently.")
        else:
            insights.append("Your productivity has remained stable.")

    if not insights:
        insights.append("Not enough data to generate insights yet.")

    return insights
