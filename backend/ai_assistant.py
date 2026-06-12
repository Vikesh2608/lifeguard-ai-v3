from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_lifeguard_ai(user_message):

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
