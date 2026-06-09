from openai import OpenAI
from racesharp.config import OPENAI_API_KEY
from racesharp.prompt import RACESHARP_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_race(race):

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": RACESHARP_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Track: {race['track']}
Time: {race['time']}

Analyse this race.
"""
            }
        ]
    )

    return response.choices[0].message.content
