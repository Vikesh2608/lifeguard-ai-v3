from openai import OpenAI
import os


def ask_lifeguard_ai(user_message):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "🤖 LifeGuard AI is currently unavailable.\n\n"
            "The OpenAI API key has not been configured yet."
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are LifeGuard AI.

    Respond with:
    - Friendly tone
    - Emojis
    - Actionable recommendations
    - Wellness advice
    - Exercise suggestions if relevant
    - Diet suggestions if relevant
    - Emergency guidance if relevant

    User:
    {user_message}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {str(e)}"
