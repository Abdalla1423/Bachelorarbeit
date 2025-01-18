from models.models import askModel
import re
from retriever.serper_retriever import google




  
def generate_questions(claim):
     return askModel(f"""
Please tell me the necessary questions that need to be answered in order to verify the following claim:

Claim: Howard University Hospital and Providence Hospital are both located in Washington, D.C.
>>>>>>
Followup Question: Where is Howard Hospital located?
Followup Question: Where is Providence Hospital located? 
------
Claim: An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.
>>>>>>
Followup Question: Which Formula 1 car was designed by Peter McCool during the 2007 Formula One season?
Followup Question: Did an IndyCar driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season?
------
Claim: Sumo wrestler Toyozakura Toshiaki committed match-fixing, ending his career in 2011 that started in 1989.
>>>>>>
Followup Question: When did Sumo wrestler Toyozakura Toshiaki ended his career?
Followup Question: What is Toyozakura Toshiaki's occupation?
Followup Question: Did Sumo wrestler Toyozakura Toshiaki committed match-fixing?
------
Claim: In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) in Chicago, United States, and the world amateur welterweight title in Mexico City.
>>>>>>
Followup Question: When was Alfredo Cornejo Cuevas born?
Followup Question: Did Alfredo Cornejo Cuevas win the gold metal in the welterweight division at the Pan American Games in 1959?
Followup Question: Where was The Pan American Games in 1959 held?
Followup Question: Did Alfredo Cornejo Cuevas win the world amateur welterweight title in Mexico City?
------
Claim: {claim}
>>>>>>
""")
     
def generate_verdict_and_explanation(claim, information):
     return askModel(f"""
Answer the following SUPPORTED / NOT_SUPPORTED questions:

Is it true that The woman the story behind Girl Crazy is credited to is older than Ted Kotcheff. ?
Let's think step by step.

Girl Crazy 's story is credited to Hampton Del Ruth.
Hampton Del Ruth was born on September 7 , 1879.
Ted Kotcheff was born on April 7 , 1931.
>>>>>>
Therefore , the answer is: [NOT_SUPPORTED]
Here are the reasons: The woman behind the story Girl Crazy is Hampton Del Ruth, who was born on September 7, 1879.
Ted Kotcheff was born on April 7, 1931. Hapmpton Del Ruth is not older than Ted Kotcheff.
------
Is it true that A hockey team calls the 70,000 capacity Madison Square Garden it's home. That team, along with the New York Islanders, and the New Jersey Devils NHL franchise, are popular in the New York metropolitan area. ?
Let's think step by step.

Madison Square Garden hosts approximately 320 events a year. It is the home to the New York Rangers of the National Hockey League.
Madison Square Garden has a capacity of 19.500.
The New York Islanders are a professional ice hockey team based in Elmont, New York. ...
>>>>>>
Therefore, the answer is: [NOT_SUPPORTED]
Here are the reasons: Madison Square Garden is the home to New York Rangers and New York Islanders. Both are popular in the New York metropolitan area.
Madison Square Garden has a capacity of 19,500, not 70,0000.
------
Is it true that The writer of the song Girl Talk and Park So-yeon have both been members of a girl group. ?
Let's think step by step.

Tionne Watkins is the writer of the song Girl Talk.
Park Soyeon is a South Korean singer. She is a former member of the kids girl group I& Girls.
Watkins rose to fame in the early 1990s as a member of the girl-group TLC
>>>>>>
Therefore, the answer is: [SUPPORTED]
Here are the reasons: Tionne Watkins is the writer of the song Girl Talk. She was a member of the girl-group TLC.
Park So-yeon is part of a girl group. Therefore, both Tioone Watkins and Park So-yeon have been members of a girl group.
------
Is it true that Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt in the German state of Hesse and the fifth-largest city in Germany. ?
Let's think step by step.

Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt.
Frankfurt is in the German state of Hesse.
Frankfurt is the fifth-largest city in Germany.
>>>>>>
Therefore, the answer is: [SUPPORTED]
Here are the reasons: Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt.
Frankfurt is in the German state of Hesse and the fifth-largest city in Germany.
------
Is it true that {claim}?
Let's think step by step:

{information}
>>>>>>
""")

def veracityPrediction(claim, qa_pairs):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with question-answer pairs regarding the following claim: {claim}
These are the provided questions and relevant answers to the question to verify the claim:
< {qa_pairs}>
Based strictly on the main claim and the question-answers provided, You have to provide:
- claim: the original claim,
- rating: choose among true, half-true and false
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format''')
     
     
def extract_rating_and_explanation(text):
    # Regular expression pattern to find the rating and explanation
    pattern = r'Therefore, the answer is: \[(.*?)\]\s*Here are the reasons:\s*(.*)'
    
    # Search for the pattern in the provided text
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the rating and explanation
    if match:
        rating = match.group(1)
        explanation = match.group(2).strip()
        return rating, explanation
    else:
        return None, None

def extract_questions(questions):
    return re.findall(r'Followup Question: (.+\?)', questions)

def folk_cot(claim):
    generated_questions = generate_questions(claim)
    extracted_questions = extract_questions(generated_questions)
    # print(extracted_questions)
    qa_pairs = grounding(extracted_questions)
    # print(answers)
    # answers = [retrieve(question) for question in questions]
    # verdict = generate_verdict_and_explanation(claim, answers)
    # rating, explanation = extract_rating_and_explanation(verdict)
    # return '{\n"claim": "' +  claim + '",\n"rating": "' + rating + '",\n"factcheck": "' + explanation.replace('"', '') + '"\n}'
    # qa_pairs = []
  
    # for question in extracted_questions:
    #     answer = retrieve(question)
    #     qa_pairs.append((question, answer))
    
    return veracityPrediction(claim, qa_pairs)


def grounding(question_list):
    qa_pairs = []
    for question in question_list:
        try:
            # print(question)
            ga = google(question)
            # ga = google(f"en.wikipedia.org {q}")
            # print(ga)
            qa_pairs.append((question,ga))
            # print(temp)
        except:
            ga = None
            qa_pairs.append((question,ga))
            continue
        # print(grounded_answers)
    return qa_pairs




# print(folk_cot('In the past two years in Congress, Alan Grayson has written more bills, passed more amendments on the floor of the House and enacted more of my bills into law than any other member of the House.'))
