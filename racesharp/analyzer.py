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
Race Data:

{race}

Analyse this race.
"""
            }
        ]
    )

    return response.choices[0].message.content


def analyze_image(image_url):

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": RACESHARP_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyse this horse racing screenshot."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content
