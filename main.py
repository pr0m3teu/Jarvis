import openai
import os
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
                "file": file_name,
                "content": text,
                "size" : len(text),
                "date": datetime.now()
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



def main():

    client = openai.OpenAI(api_key=OPENAI_KEY)

#    response = client.responses.create(
#        model="gpt-5-nano",
#        reasoning={"effort": "low"},
#        input="What should I build with this OpenAI key I'm using right now?",
#    )

    chunks = index_file("test.txt")
    for chunk in chunks:
        print(chunk)

    indexed_chunks = index_folder("../../train-data/")
    print(indexed_chunks)


if __name__ == "__main__":
    main()


