import openai
import os
import sqlite3
from dotenv import load_dotenv

from indexing import index_folder, chunk_from_entry
from infer import infer


load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

def main():
    client = openai.OpenAI(api_key=OPENAI_KEY)
    indexed_chunks = index_folder("../../train-data/")

    res = infer(client, "Who are you?")
    print(res)


if __name__ == "__main__":
    main()


