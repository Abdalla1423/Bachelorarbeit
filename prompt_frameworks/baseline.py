from models.models import askModel
import re
import json
import ast

def base(claim):
    return base_averitec(claim)

def base_politifact(claim):
  claimant, pureclaim = claim.split("says", 1)
  result = askModel(f'''You are a well-informed and expert fact-checker.
You are provided with the following claim claim made by {claimant} : {pureclaim}

Based on the main claim and your knowledge, You have to provide:
- claim: the original claim,
- label: choose between true, false and NEI(not enough information),
- explanation: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format without any additional characters and don't surrond the json with backticks!''')
  return result.replace("\n", "")

def base_averitec(claim):
  result = askModel(f''' Decide if the last claim is supported, refuted or if nei (not enough information) using your own knowledge. Explain the reasoning step-by-step
before giving the answer. 
Generate the output in form of a json as shown in the example below.
----- Examples:
Claim: South Africans that drink are amongst the top drinkers in the world.
Output: {{
"explanation": "The claim stays amongst the top drinkers not the top first, so since they are 6th, this could be
plausible. The answer is support.",
"label": "supported"
}}
Claim: All government schools in India are being privatised.
Output: {{
"explanation": "There is no plan by the Indian government to privatize primary education as said by the Minister of
Human Resource Development. The claim is clearly refuted and therefore the answer is refute.",
"label": "refuted"
}}
Claim: {claim}    
Output:''')
  extracted_result = get_last_json_object(result)
  return extracted_result

def get_last_json_object(text):
    """
    Extract and return the last JSON object of the form
    {
      "label": "...",
      "explanation": "..."
    }
    from the given text.

    Returns:
        A dictionary representing the parsed JSON if successful, or None if no match is found
        or if parsing fails.
    """
    # Regex Explanation:
    #   - We look for an opening brace '{'
    #   - Then "label" : "<some text>"
    #   - Then "explanation" : "<some text>"
    #   - Dotall flag (re.DOTALL) allows '.' to match newlines as well.
    pattern = re.compile(
        r'(\{\s*"(?:label|explanation)"\s*:\s*".+?"\s*,\s*"(?:label|explanation)"\s*:\s*".+?"\s*\})',
        re.DOTALL
    )


    matches = pattern.findall(text)
    if not matches:
        return None  # No JSON object found that matches our pattern

    # The last matching JSON block as a string
    last_json_str = matches[-1]

    return last_json_str
  
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

