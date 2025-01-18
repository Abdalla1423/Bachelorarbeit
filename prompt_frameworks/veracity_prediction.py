from models.models import askModel

def veracityPrediction(claim, information):
  claimant, pureclaim = claim.split("says", 1)
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with information regarding the following claim made by {claimant}: {pureclaim}
These is the provided information to verify the claim:
< {information}>
Based on the main claim and the information provided, You have to provide:
- claim: the original claim,
- rating: choose between true, false and NEI(not enough information),
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format without any additional characters and don't surrond the json with backticks!''')