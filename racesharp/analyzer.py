from openai import OpenAI

from racesharp.config import OPENAI_API_KEY
from racesharp.prompt import RACESHARP_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_race(race):

    race_data = f"""
Track: {race['track']}
Time: {race['time']}
Status: {race['status']}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
{RACESHARP_PROMPT}

RACE DATA

{race_data}
"""
    )

    return response.output_text
