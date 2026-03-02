import openai
import os
import sqlite3
import uuid
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

def index_file(file_name: str) -> list[dict]:
    chunks = []
    with open(file_name, "r") as f:
        while True:
            text = f.read(500)
            if not text:
                break

            chunks.append({
                "id": str(uuid.uuid4()),
                "file": file_name,
                "content": text,
                "size" : len(text),
                "date": str(datetime.now())
            })

    return chunks


def index_folder(folder_name: str) -> list[dict]:
    indexed_chunks = []
    for fd in os.listdir(folder_name):
        file_path = folder_name + fd
        if fd.endswith(".pdf"):
            continue

        if os.path.isdir(file_path):
            continue

        indexed_chunks.append(index_file(file_path))
        
    indexed_chunks = [chunk for sublist in indexed_chunks for chunk in sublist]
    return indexed_chunks


def save_embeddings_to_db(con: sqlite3.Connection, client, chunks: list[dict]) -> None:
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY, file TEXT NOT NULL, content TEXT NOT NULL, embedding BLOB, size INT, date DATETIME)")

    for chunk in chunks:
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk["content"]
            )
            chunk["embedding"] = response.data[0].embedding

            chunk_fields = (chunk["id"], chunk["file"], chunk["content"], chunk["embedding"], chunk["size"], chunk["date"])
            cursor.execute("INSERT INTO chunks (id, file, content, embedding, size, date) VALUES (?, ?, ?, ?, ?, ?)", chunk_fields)

        except Exception as e:
            print(e)


def main():
    client = openai.OpenAI(api_key=OPENAI_KEY)

    indexed_chunks = index_folder("../../train-data/")

    con = sqlite3.connect("memory.db")
    save_to_db(con, indexed_chunks)

    con.commit()
    con.close()


if __name__ == "__main__":
    main()


