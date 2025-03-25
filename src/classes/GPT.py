from openai import OpenAI
from src.functions.utils import print_verbose
import os
from dotenv import load_dotenv

load_dotenv()

class GPT:
    def __init__(self):
        pass

    def print_verbose(self, text):
        print_verbose(
            text,
            os.getenv("verbose"),
            os.getenv("gpt_verbose_color"),
            os.getenv("gpt_verbose_labe")
        )

    def ask_gpt(self, prompt):
        self.print_verbose(f"Function: ask_gpt")
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        completion = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        self.print_verbose(completion.choices[0].message.content)
        return str(completion.choices[0].message.content)

