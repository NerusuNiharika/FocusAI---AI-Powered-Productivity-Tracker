from google import genai
from dotenv import load_dotenv
import os
import random
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "gemini-2.5-flash"

# ---------------- FALLBACK RESPONSES ----------------

fallback_responses = [
    "Stay focused. Small improvements matter.",
    "Consistency builds productivity over time.",
    "Try focusing for the next 20 minutes.",
    "Reducing distractions improves deep work.",
    "You're making progress. Keep going."
]

# ---------------- COMMON AI FUNCTION ----------------

def ask_ai(prompt):

    try:

        time.sleep(3)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("Gemini API Error:", e)

        return random.choice(fallback_responses)


# ---------------- DASHBOARD AI MESSAGE ----------------

def get_ai_message(total_duration):

    prompt = f"""
    You are an AI productivity assistant.

    Total distraction time today:
    {total_duration} minutes

    Generate one short motivational productivity insight.

    Rules:
    - Keep it under 25 words
    - Friendly tone
    - No emojis
    """

    return ask_ai(prompt)


# ---------------- CHATBOT RESPONSE ----------------

def respond_to_user_message(user_message, total_duration):

    prompt = f"""
    User says:
    {user_message}

    Their distraction time today is:
    {total_duration} minutes

    Respond like a supportive productivity assistant.

    Rules:
    - Keep response short
    - Friendly and motivating
    - No emojis
    """

    return ask_ai(prompt)


# ---------------- ANALYTICS INSIGHTS ----------------

def generate_analytics_insight(
    category_data,
    time_slot_data,
    productivity_data,
    daily_data
):

    prompt = f"""
    Analyze this productivity data.

    Category Data:
    {category_data}

    Time Slot Data:
    {time_slot_data}

    Productivity Scores:
    {productivity_data}

    Daily Data:
    {daily_data}

    Generate 4 short productivity insights.

    IMPORTANT:
    - No numbering
    - No bullet points
    - One sentence per line
    - Professional tone
    """

    response = ask_ai(prompt)

    insights = response.split("\n")

    cleaned = []

    for insight in insights:

        insight = insight.strip()

        if insight:
            cleaned.append(insight)

    return cleaned


