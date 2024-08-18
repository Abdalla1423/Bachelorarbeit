from models.models import askModel

def baseline(claim):
    prompt = f'''Given the following statement, determine if it is false, true.
    Only reply with either false, true. Reply with failed if you don't know. Statement: {claim}
    '''   
    return askModel(prompt)

print(baseline('My name is Li'))
