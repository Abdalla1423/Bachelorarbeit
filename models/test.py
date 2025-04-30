from openai import OpenAI

# API configuration
api_key = 'ace0b273a98ae4ab26103f97a775bdf1'  # Replace with your API key
base_url = "https://chat-ai.academiccloud.de/v1"
model = "deepseek-r1"  # Choose any available model

# Start OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Get response
chat_completion = client.chat.completions.create(
    messages=[{"role": "system", "content": "You are a helpful assistant"}, {
        "role": "user", "content": "Which model are you and who devloped you?"}],
    model=model,
)

# Print full response as JSON
# You can extract the response text from the JSON object
print(chat_completion.choices[0].message.content)
