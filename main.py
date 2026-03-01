import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

def main():
    client = openai.OpenAI(
        api_key=OPENAI_KEY
    )

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        input="What should I build with this OpenAI key I'm using right now?",
    )

    print(response.output_text)


if __name__ == "__main__":
    main()