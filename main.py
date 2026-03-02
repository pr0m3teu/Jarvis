import openai
import os
import sqlite3
from dotenv import load_dotenv

from indexing import index_folder, chunk_from_entry

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

def main():
    client = openai.OpenAI(api_key=OPENAI_KEY)
    indexed_chunks = index_folder("../../train-data/")

    con = sqlite3.connect("memory.db")
    # save_embeddings_to_db(con, client, indexed_chunks)
    cursor = con.cursor()
    res = cursor.execute("SELECT * FROM chunks")
    for entry in res.fetchall():
        chunk = chunk_from_entry(entry)
        print(chunk)

    con.close()


if __name__ == "__main__":
    main()


