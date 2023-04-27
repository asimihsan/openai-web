import openai
import openai.error
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

        # If we get openai.error.InvalidRequestError with 'This model's maxium context length', then we will try up to 2 more
        # times and half the max_tokens each time. If all three attempts fail we will respond with text 'Error: max context length'
        # and log the error.
        tokens_schedule = [max_tokens, max_tokens // 2, max_tokens // 4]
        success = False
        response: openai.ChatCompletion | None = None
        for tokens in tokens_schedule:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{
                        "role": "user",
                        "content": prompt,
                    }],
                    max_tokens=tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stream=True,
                )
                success = True
                break
            except openai.error.InvalidRequestError as e:
                if "This model's maximum context length" in e._message:
                    continue
                else:
                    raise e

        if not success:
            return "Error: max context length"

        for chunk in response:
            choice = chunk["choices"][0]
            finish_reason = choice["finish_reason"] # None, "stop", or "length"
            delta = choice["delta"]

            if "role" in delta and delta["role"] == "assistant":
                continue

            if finish_reason is None:
                yield delta["content"]

        return ""

