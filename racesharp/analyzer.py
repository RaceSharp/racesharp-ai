try:

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
        ],
        max_tokens=1500
    )

    return response.choices[0].message.content

except Exception as e:

    return f"RaceSharp Error:\n\n{str(e)}"
