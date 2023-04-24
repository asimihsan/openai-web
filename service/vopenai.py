import openai
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIWrapper:
    def __init__(self):
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment variables")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def complete(self, prompt, max_tokens=2048, temperature=0.0, top_p=1, frequency_penalty=0, presence_penalty=0):
        print(prompt)
        response = openai.ChatCompletion.create(
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
            stream=True,
        )
        for chunk in response:
            choice = chunk["choices"][0]
            finish_reason = choice["finish_reason"] # None, "stop", or "length"
            delta = choice["delta"]

            if "role" in delta and delta["role"] == "assistant":
                continue

            if finish_reason is None:
                yield delta["content"]

        return ""

