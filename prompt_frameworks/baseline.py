from models.models import askModel
from prompt_frameworks.veracity_prediction import get_last_json_object

# The baseline approach predicts claim veracity based solely on the claim text, without external evidence.
# This prompt formulation is adapted from Akhtar et al. (2024).


def base(claim):
    result = askModel(f''' Decide if the last claim is supported, refuted or if nei (not enough information) using your own knowledge. Explain the reasoning step-by-step
    before giving the answer. For the label, choose between "supported", "refuted", or "NEI" (not enough information).
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
