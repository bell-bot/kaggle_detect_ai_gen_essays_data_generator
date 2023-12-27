def query_chatgpt(prompt, n, client):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        n=n
    )
    return completion
