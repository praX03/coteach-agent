import os  # Included to Python

import openai
from dotenv import load_dotenv

load_dotenv()


def handle_image(url, query=None):
    print(url, query, "openai api key", os.getenv("OPENAI_API_KEY"))
    client = openai
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query,
                    },
                    {
                        "type": "image_url",
                        "image_url": url,
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
