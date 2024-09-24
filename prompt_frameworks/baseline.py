from models.models import askModel
import re
from models.models import askLlama

def base(claim):
  result = askModel(f'''You are a well-informed and expert fact-checker.
You are provided with the following claim: {claim}

Based on the main claim and your knowledge, You have to provide:
- claim: the original claim,
- rating: choose between true and false,
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format and no other characters''')
  # print(result)
  return result.replace("\n", "")
  
def fewshot(claim):
     return askModel(f"""
Please verify the following claim and provide explanations:

Claim: The woman the story behind Girl Crazy is credited to is older than Ted Kotcheff.
>>>>>>
This claim is: [REFUTED]
Here are the reasons: The woman behind the story Girl Crazy is Hampton Del Ruth, who was born on September 7, 1879.
Ted Kotcheff was born on April 7, 1931. Hapmpton Del Ruth is not older than Ted Kotcheff.
------
Claim: A hockey team calls the 70,000 capacity Madison Square Garden it's home. That team, along with the New York Islanders, and the New Jersey Devils NHL franchise, are popular in the New York metropolitan area.
>>>>>>
This claim is: [REFUTED]
Here are the reasons: Madison Square Garden is the home to New York Rangers and New York Islanders. Both are popular in the New York metropolitan area.
Madison Square Garden has a capacity of 19,500, not 70,0000.
------
Claim: The writer of the song Girl Talk and Park So-yeon have both been members of a girl group.
>>>>>>
This claim is: [SUPPORTED]
Here are the reasons: Tionne Watkins is the writer of the song Girl Talk. She was a member of the girl-group TLC.
Park So-yeon is part of a girl group. Therefore, both Tioone Watkins and Park So-yeon have been members of a girl group.
------
Claim: Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt in the German state of Hesse and the fifth-largest city in Germany.
>>>>>>
This claim is: [SUPPORTED]
Here are the reasons: Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt.
Frankfurt is in the German state of Hesse and the fifth-largest city in Germany.
------
Claim: {claim}
>>>>>>
""")
     
     
def extract_rating_and_explanation(text):
    # Regular expression pattern to find the rating and explanation
    pattern = r'This claim is: \[(.*?)\]\s*Here are the reasons:\s*(.*)'
    
    # Search for the pattern in the provided text
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the rating and explanation
    if match:
        rating = match.group(1)
        explanation = match.group(2).strip()
        return rating, explanation
    else:
        return None, None

def base_fewshot(claim):
    result = fewshot(claim)
    rating, explanation = extract_rating_and_explanation(result)
    return '{\n"claim": "' +  claim + '",\n"rating": "' + rating + '",\n"factcheck": "' + explanation.replace('"', '') + '"\n}'

# print(base('David Cicilline was the state representative who opposed tough mandatory sentences for those convicted of domestic violence  and child abuse.'))