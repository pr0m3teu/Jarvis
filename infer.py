MODEL = "gpt-5-mini-2025-08-07"


def infer(client, msg : str) -> str:
    response = client.responses.create(
            model=MODEL,
            input=msg
    )
    
    return response.output_text

