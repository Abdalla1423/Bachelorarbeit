from openai import OpenAI
import ollama


def askLlamaVllm(prompt, stopSeq):
    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:5000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        stop=stopSeq
    )

    return completion.choices[0].message.content

def askLlamaKISS(prompt, stopSeq):
    openai_api_key = "ace0b273a98ae4ab26103f97a775bdf1"
    openai_api_base = "https://chat-ai.academiccloud.de/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    completion = client.chat.completions.create(
        model="llama-3.3-70b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        stop=stopSeq
    )

    return completion.choices[0].message.content

from openai import OpenAI


def askLlamaOllama(prompt, stopSeq):
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ],
        stream=False,
        options={"stop": stopSeq}
    )
    return response['message']['content']