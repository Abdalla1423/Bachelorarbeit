from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = [ 
    {"role": "user", "content": '''
You are given a piece of text that includes knowledge
claims. A claim is a statement that asserts something
as true or false, which can be verified by humans.
[Task]
Your task is to accurately identify and extract every
claim stated in the provided text. Then, resolve any
coreference (pronouns or other referring expressions)
in the claim for clarity. Each claim should be concise
(less than 15 words) and self-contained.
Your response MUST be a list of dictionaries. Each
dictionary should contains the key "claim", which
correspond to the extracted claim (with all coreferences resolved). You MUST only respond in the format as described below. DO NOT RESPOND WITH
ANYTHING ELSE. ADDING ANY OTHER EXTRA
NOTES THAT VIOLATE THE RESPONSE FORMAT
IS BANNED. START YOUR RESPONSE WITH '['.
[Response Format]
[{"claim": "Ensure that the claim is fewer than 15
words and conveys a complete idea. Resolve any coreference (pronouns or other referring expressions) in the
claim for clarity." },... ]
Here are two examples:
[text]:
Tomas Berdych defeated Gael Monfis 6-1, 6-4 on Saturday. The sixth-seed reaches Monte Carlo Masters
final for the first time . Berdych will face either Rafael
Nadal or Novak Djokovic in the final.
[response]:
[{"claim": "Tomas Berdych defeated Gael Monfis 6-1, 6-4"}, {"claim": "Tomas Berdych defeated
Gael Monfis 6-1, 6-4 on Saturday"}, {"claim":
"Tomas Berdych reaches Monte Carlo Masters final"}, {"claim": "Tomas Berdych is the sixth-seed"},
{"claim": "Tomas Berdych reaches Monte Carlo Masters final for the first time"}, {"claim": "Berdych
will face either Rafael Nadal or Novak Djokovic"},
{"claim": "Berdych will face either Rafael Nadal or
Novak Djokovic in the final"}]
[text]:
Tinder only displays the last 34 photos - but users can
easily see more. Firm also said it had improved its
mutual friends feature.
[response]:
[{"claim": "Tinder only displays the last photos"},
{"claim": "Tinder only displays the last 34 photos"},
{"claim": "Tinder users can easily see more photos"},
{"claim": "Tinder said it had improved its feature"},
{"claim": "Tinder said it had improved its mutual
friends feature"}]
Now complete the following:
[text]:
Both James Cameron and the director of the film Interstellar were born in Canada
[response]:
     '''}
  ]
)

print(completion.choices[0].message)