from models.models import askModel
import re

def veracityPrediction(claim, information):
  return proxy_ref_vp(claim, information)

def ragar_vp(claim, information):
  claimant, pureclaim = claim.split("says", 1)
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with information regarding the following claim made by {claimant}: {pureclaim}
These is the provided information to verify the claim:
< {information}>
Based on the main claim and the information provided, You have to provide:
- claim: the original claim,
- label: choose between true, false and NEI(not enough information),
- explanation: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format without any additional characters and don't surrond the json with backticks!''')

def proxy_ref_vp(claim, information):
  result = askModel(f''' 
Decide if the evidence supports the last given claim, refutes it, or doesn't give enough information. Explain the reasoning step-by-step
before giving the answer. Only use the provided information and no additional sources or background knowledge.
Generate the output in form of a json as shown in the example below.
----- Examples:
Claim: South Africans that drink are amongst the top drinkers in the world.
Evidence: What is the global average alcohol consumption in litres of pure alcohol per day? The global averages as of 2016
is 15.1 litres per day. What is the daily average of pure alcohol consumption per day in South africa? 29.9 litres. Where does
South Africa rank as a nation in terms of Daily pure Alcohol consumption? 6th out of 189 countries.
Output: {{
"explanation": "The claim stays amongst the top drinkers not the top first, so since they are 6th, this could be
plausible. The answer is support.",
"label": "supported"
}}
Claim: All government schools in India are being privatised.
Evidence: What did India's Union Education Minister say about the privatisation of governments schools? New Delhi: There
is no plan to privatise primary education, the Centre told the Parliament today. This statement was given by Minister of
Human Resource Development,
Ramesh Pokhriyal Nishank in the Lok Sabha today in response to Kaushalendra Kumar question on whether it is fact that
NITI Aayog has suggested that Primary Education may be given to the private sector to reduce the burden of salary to
teachers and other infrastructure.
Output: {{
"explanation": "There is no plan by the Indian government to privatize primary education as said by the Minister of
Human Resource Development. The claim is clearly refuted and therefore the answer is refute.",
"label": "refuted"
}}
Claim: {claim}    
Evidence: {information}
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

    print("TEXT", text)

    matches = pattern.findall(text)
    if not matches:
        return None  # No JSON object found that matches our pattern

    print("MATCHES", matches)
    # The last matching JSON block as a string
    last_json_str = matches[-1]

    return last_json_str