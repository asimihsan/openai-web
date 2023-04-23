import openai
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIWrapper:
    def __init__(self):
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment variables")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def complete(self, prompt, max_tokens=10, temperature=0.0, top_p=1, frequency_penalty=0, presence_penalty=0):
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        return response.choices[0].message.content
