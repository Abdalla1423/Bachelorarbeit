from openai import OpenAI
import json

claim = 'State lawmakers are spending taxpayer money for parking that billionaire Arthur Blank could build while paying some state employees so little they are on food stamps.'
prompt = f'''You are a well-informed and expert fact-checker.
You are provided with the following claim: "{claim}"

Based on the main claim and your knowledge, you must provide:
- "claim": the original claim,
- "rating": choose among "true", "half-true", and "false" only,
- "factcheck": a concise and detailed fact-check paragraph.

Please output your response in the following JSON format and output nothing else:

{{
  "claim": "...",
  "rating": "...",
  "factcheck": "..."
}}
'''

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:5000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
completion = client.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    prompt=prompt,
    max_tokens=215,
    temperature=0,
)

# Parse the output to extract the JSON object
output = completion.choices[0].text.strip()

try:
    # Attempt to parse the JSON from the output
    result = json.loads(output)
    print("Completion result:", result)
except json.JSONDecodeError:
    print("Failed to parse JSON:", output)
