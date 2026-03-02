import os
import numpy as np
import sqlite3
import uuid
from datetime import datetime


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
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            print(embedding)

            chunk_fields = (chunk["id"], chunk["file"], chunk["content"], embedding.tobytes(), chunk["size"], chunk["date"])
            cursor.execute("INSERT INTO chunks (id, file, content, embedding, size, date) VALUES (?, ?, ?, ?, ?, ?)", chunk_fields)
            print("Saved Chunk!\n")

        except Exception as e:
            print(e)

    con.commit()


def chunk_from_entry(entry):
    return {
            "id": entry[0],
            "file": entry[1],
            "content": entry[2],
            "embedding": np.frombuffer(entry[3], dtype=np.float32),
            "size": entry[4],
            "date": entry[5],
        }


