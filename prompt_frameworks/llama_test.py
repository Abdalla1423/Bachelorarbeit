import json
from models.models import askLlama

claim = 'State lawmakers are spending taxpayer money for parking that billionaire Arthur Blank could build while paying some state employees so little they are on food stamps.'
prompt = f'''You are a well-informed and expert fact-checker.
You are provided with the following claim: "{claim}"

Based on the main claim and your knowledge, you must provide:
- "claim": the original claim,
- "rating": choose among "true", "half-true", and "false" only,
- "factcheck": a concise and detailed fact-check paragraph.

Please output your response in the following JSON format.
'''

# Parse the output to extract the JSON object
output = askLlama(prompt=prompt)

try:
    # Attempt to parse the JSON from the output
    result = json.loads(output)
    print("Completion result:", result)
except json.JSONDecodeError:
    print("Failed to parse JSON:", output)
