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
