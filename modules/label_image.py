# https://platform.openai.com/docs/guides/vision
# !export OPENAI_API_KEY=your_openai_api_key

import openai

def text_recognition(image_url):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Perform Optical Character Recognition and output the text in the image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    text_ocr = response.choices[0].message.content
    return text_ocr