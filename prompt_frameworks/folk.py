from models.models import askModel
import re
from retriever.serper_retriever import google
from retriever.retriever import retrieve

def generate_questions(claim):
    return askModel(
f"""You are given a problem description and a claim. The task is to:
1) define all the predicates in the claim
2) parse the predicates into followup questions
3) answer the followup questions

Claim: Howard University Hospital and Providence Hospital are both located in Washington, D.C.
>>>>>>
Predicates:
Location(Howard Hospital, Washington D.C.) ::: Verify Howard University Hospital is located in Washington, D.C.
Location(Providence Hospital, Washington D.C.) ::: Verify Providence Hospital is located in Washington, D.C.

Followup Question: Where is Howard Hospital located?
Followup Question: Where is Providence Hospital located? 
------
Claim: An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.
>>>>>>
Predicates: 
Designed(Peter McCool, a Formula 1 car) ::: Verify a Formula 1 car was designed by Peter McCool during the 2007 Formula One season.
Drive(An IndyCar race driver, a Formula 1 car) ::: Verify an IndyCar driver drove a Formula 1 car.

Followup Question: Which Formula 1 car was designed by Peter McCool during the 2007 Formula One season?
Followup Question: Did an IndyCar driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season?
------
Claim: Thomas Loren Friedman has won more Pulitzer Prizes than Colson Whitehead
>>>>>>
Predicates: 
Won(Thomas Loren Friedman, Pulitzer Prize) ::: Verify the number of Pulitzer Prizes Thomas Loren Friedman has won.
Won(Colson Whitehead, Pulitzer Prize) ::: Verify the number of Pulitzer Prizes Colson Whitehead has won.

Followup Question: How many Pulitzer Prize did Thomas Loren Friedman win?
Followup Question: How many Pulitzer Prize did Colson Whitehead win?
------
Claim: SkyHigh Mount Dandenong (formerly Mount Dandenong Observatory) is a restaurant located on top of Mount Dandenong, Victoria, Australia.
>>>>>>
Predicates:
Location(SkyHigh Mount Dandenong, top of Mount Dandenong, Victoria, Australia) ::: Verify that SkyHigh Mount Dandenong is located on top of Mount Dandenong, Victoria, Australia.
Known(SkyHigh Mount Dandenong, Mount Dandenong Observatory) ::: Verify that SkyHigh Mount Dandenong is formerly known as Mount Dandenong Observatory.

Followup Question: Where is SkyHigh Mount Dandenong located?
Followup Question: Was SkyHigh Mount Dandenong formerly known as Mount Dandenong Observatory? 
------
Claim: Shulin, a 33.1288 km (12.7911 sq mi) land located in New Taipei City, China, a country in East Asia, has a total population of 183,946 in December 2018.
>>>>>>
Predicates: 
Location(Shulin, New Taipei City, Chian) ::: Verify that Shulin is located in New Taipei City, China.
Population(Shulin, 183,946) ::: Verify that Shulin has a total population of 183,946 in December 2018.

Followup Question: Where is Shulin located?
Followup Question: What is the population of Shulin?
------
Claim: Sumo wrestler Toyozakura Toshiaki committed match-fixing, ending his career in 2011 that started in 1989.
>>>>>>
Predicates: 
Ending(Toyozakura Toshiaki, his career in 2011) ::: Verify that Toyozakura Toshiaki ended his career in 2011.
Occupation(Toyozakura Toshiaki, sumo wrestler) ::: Verify that Toyozakura Toshiaki is a sumo wrestler.
Commit(Toyozakura Toshiaki, match-fixing) ::: Verify that Toyozakura Toshiaki committed match-fixing.

Followup Question: When did Sumo wrestler Toyozakura Toshiaki ended his career?
Followup Question: What is Toyozakura Toshiaki's occupation?
Followup Question: Did Sumo wrestler Toyozakura Toshiaki committed match-fixing?
------
Claim: In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) in Chicago, United States, and the world amateur welterweight title in Mexico City.
>>>>>>
Predicates: 
Born(Alfredo Cornejo Cuevas, June 6 1933) ::: Verify that Alfredo Cornejo Cuevas was born June 6 1933. 
Won(Alfredo Cornejo Cuevas, the gold metal in the welterweight division at the Pan American Games in 1959) ::: Verify that Alfredo Cornejo Cuevas won the gold metal in the welterweight division at the Pan American Games in 1959.
Held(The Pan American Games in 1959, Chicago United States) ::: Verify that The Pan American Games in 1959 was held in Chicago United States.
Won(Alfredo Cornejo Cuevas, the world amateur welterweight title in Mexico City).

Followup Question: When was Alfredo Cornejo Cuevas born?
Followup Question: Did Alfredo Cornejo Cuevas win the gold metal in the welterweight division at the Pan American Games in 1959?
Followup Question: Where was The Pan American Games in 1959 held?
Followup Question: Did Alfredo Cornejo Cuevas win the world amateur welterweight title in Mexico City?
------
Claim: The birthplace of American engineer Alfred L.Rives is a plantation near Monticello, the primary residence of Thomas Jefferson.
>>>>>>
Predicates:
Birthplace(Alfred L. Rives, a plantation) ::: Verify The birthplace of American engineer Alfred L.Rives is a plantation
Primary residence(Thomas Jefferson, Monticello) ::: Verify Monticello, the primary residence of Thomas Jefferson. 
Near(a planation, Monticello) ::: Verify A plantation is near Monticello

Followup Question: Where is the birthplace of Alfred L. Rives? 
Followup Question: Where is the primary residence of Thomas Jefferson? 
Followup Question: Is the birthplace of Alfred L. Rives near the residence of Thomas Jefferson? 
------
Claim: {claim}
>>>>>>
""")
    
def veracityPrediction_(claim, qa_pairs):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with question-answer pairs regarding the following claim: {claim}
These are the provided questions and relevant answers to the question to verify the claim:
< {qa_pairs}>
Based strictly on the main claim and the question-answers provided, You have to provide:
- claim: the original claim,
- rating: choose among true, half-true and false
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format''')


def veracityPrediction(claim, qa_pairs):
    return askModel(
        f"""
Given a question and a context, provide a [SUPPORTED] or [NOT_SUPPORTED] answer and explain why.

Question: 
Is it true that The writer of the song Girl Talk and Park So-yeon have both been members of a girl group.?

Context:
Write(the writer, the song Girl Talk) ::: Verify that the writer of the song Girl Talk
Member(Park So-yeon, a girl group) ::: Verify that Park So-yeon is a memeber of a girl group
Member(the writer, a girl group) ::: Verify that the writer of the song Girl Talk is a member of a gril group

Who is the writer of the song Girl Talk? Tionne Watkins is the writer of the song Girl Talk.
Is Park So-yeon a member of a girl group? Park Soyeon is a South Korean singer. She is a former member of the kids girl group I& Girls.
Is the writer of the song Girl Talk a member of a girl group? Watkins rose to fame in the early 1990s as a member of the girl-group TLC
>>>>>>
Prediction:
Write(Tionne Watkins, the song Girl Talk) is True because Tionne Watkins is the writer of the song Girl Talk.
Member(Park So-yeon, a girl group) is True because Park Soyeon is a South Korean singer. She is a former member of the kids girl group I& Girls.
Member(Tionne Watkins, a girl group) is True because Watkins rose to fame in the early 1990s as a member of the girl-group TLC
Write(Tionne Watkins, the song Girl Talk) && Member(Park So-yeon, a girl group) && Member(Tionne Watkins, a girl group) is True.
The claim is [SUPPORTED].

Explanation:
Tionne Watkins, a member of the girl group TLC in the 1990s, is the writer of the song "Girl Talk." 
Park Soyeon, a South Korean singer, was formerly part of the girl group I& Girls. 
Therefore, both Watkins and Park Soyeon have been members of girl groups in their respective careers.
------
Question:
Is it true that A hockey team calls the 70,000 capacity Madison Square Garden it's home. That team, along with the New York Islanders, and the New Jersey Devils NHL franchise, are popular in the New York metropolitan area.?

Context:
Home(a hocky team, Madison Square Garden) ::: Verify that a hockey team calls Madison Square Garden its home.
Capacity(Madison Square Garden, 70,000) ::: Verify that Madison Square Garden has capacity of 70,000.
Popular(New York Islanders, New York Metropolitan area) ::: Verify that New York Islanders are popular in the New York metropolitan area.

Which hocky team calls Madison Square Garden Home? Madison Square Garden hosts approximately 320 events a year. It is the home to the New York Rangers of the National Hockey League
What is the capacity of Madison Square Garden? Madison Square Garden has a capacity of 19.500.
Is New York Islanders popular in New York Metropolitan area? The New York Islanders are a professional ice hockey team based in Elmont, New York. ... 
>>>>>>
Prediction:
Home(New York Rangers, Madison Square Garden) is True because Madison Square Garden hosts approximately 320 events a year. It is the home to the New York Rangers of the National Hockey League
Capacity(Madison Square Garden, 70,000) is False because Madison Square Garden has a capacity of 19.500.
Popular(New York Islanders, New York Metropolitan area) is True because The New York Islanders are a professional ice hockey team based in Elmont, New York. ...
Home(New York Rangers, Madison Square Garden) && Capacity(Madison Square Garden, 70,000) && Popular(New York Islanders, New York Metropolitan area) is False.
The claim is [NOT_SUPPORTED].

Explanation:
The New York Rangers, along with the New York Islanders and the New Jersey Devils, are popular National Hockey League (NHL) teams in the New York metropolitan area. 
Madison Square Garden, a well-known venue in New York City, has a capacity of approximately 19,500, not 70,000.
------
Question: 
Is it true that Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt in the German state of Hesse and the fifth-largest city in Germany.?

Context:
Born(Werner Gunter Jaff\u00e9 Fellner, Frankfurt)
State(Frankfurt, the German state of Hesse)

Where was Werner Gunter Jaff\u00e9 Fellner born? Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt.
Which state is Frankfurt in? Frankfurt is in the German state of Hesse.
>>>>>>
Prediction:
Born(Werner Gunter Jaff\u00e9 Fellner, Frankfurt) is True because Werner Gunter Jaff\u00e9 Fellner was born in Frankfurt.
State(Frankfurt, the German state of Hesse) is True because Frankfurt is in the German state of Hesse.
Born(Werner Gunter Jaff\u00e9 Fellner, Frankfurt) && State(Frankfurt, the German state of Hesse) is True.
The claim is [SUPPORTED].

Explanation:
Werner Gunter Jaffé Fellner was born in Frankfurt, which is both in the German state of Hesse and the fifth-largest city in Germany.
------
Question:
Is it true that The American lyricist Tom Jones,  born in 1928, co-authored the screenplay for the musical film The Fantastics.?

Context:
Born(Tom Jones, 1928)
Nationality(Tom Jones, American)
Co-author(Tome Jones, the musical film The Fantastics)

When was Tom Jones born? Thomas Jones Woodward was born in Pontypridd, South Wales, Great Britain on June 7, 1940
What is Tome Jones nationality? Sir Thomas Jones Woodward OBE is a Welsh singer. 
Who co-author the musical film The Fantastics? Tome Jones co-authored the musical film The Fantastics.
>>>>>>
Prediction:
Born(Tom Jones, 1928) is False because Thomas Jones Woodward was born in Pontypridd, South Wales, Great Britain on June 7, 1940
Nationality(Tom Jones, American) is False because Thomas Jones Woodward is a British singer. 
Co-author(Tome Jones, the musical film The Fantastics) is True because Tome Jones co-authored the musical film The Fantastics.
Born(Tom Jones, 1928) && Nationality(Tom Jones, American) && Co-author(Tome Jones, the musical film The Fantastics) is False.
The claim is [NOT_SUPPORTED].

Explanation:
Thomas Jones Woodward was born in Pontypridd, South Wales, Great Britain on June 7, 1940. He is a british singer.
Thomas Jones co-authored the musical film The Fantastics.
------
Question: Is it true that {claim}?

Context: 
{qa_pairs}
>>>>>>
"""
    )

def extract_questions(questions):
    return re.findall(r'Followup Question: (.+\?)', questions)

def grounding(question_list):
    qa_pairs = []
    for question in question_list:
        try:
            # print(question)
            ga = retrieve(question)
            # ga = google(f"en.wikipedia.org {q}")
            # print(ga)
            qa_pairs.append((question,", ".join(ga)))
            # print(temp)
        except:
            ga = "No results found"
            qa_pairs.append((question, ga))
            continue
        # print(grounded_answers)
    
    return qa_pairs


def extract_predicates(text):
     # Define the pattern to match predicates
    pattern = r".*:::\s.*"
    
    # Find all predicates using regex
    predicates = re.findall(pattern, text)
    
    return predicates

def extract_rating_and_explanation(text):
    # Define patterns to match the veracity label and the explanation
    veracity_pattern = r"\[(.*?)\]"
    explanation_pattern = r"Explanation:\n(.*)"

    # Find the veracity label
    veracity_match = re.search(veracity_pattern, text)
    veracity_label = veracity_match.group(1) if veracity_match else "Veracity label not found"
    
    # Find the explanation
    explanation_match = re.search(explanation_pattern, text, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else "Explanation not found"
    
    return veracity_label, explanation

def folk(claim):
    generated_questions = generate_questions(claim)
    # print(generated_questions)
    # print()
    extracted_questions = extract_questions(generated_questions)
    extracted_predicates = extract_predicates(generated_questions)
    # print(extracted_predicates)
    # print(extracted_questions)
    # print()
    qa_pairs = grounding(extracted_questions)
    # print(qa_pairs)
    # print()
    # qa_pairs_mod = [", ".join(pair) for pair in qa_pairs]
    # qa_pairs_mod = "\n".join(qa_pairs_mod)
    # veracity_text = "\n".join(extracted_predicates) + "\n\n" + qa_pairs_mod
    # prediction = veracityPrediction(claim, veracity_text)
    # label, explanation = extract_rating_and_explanation(prediction)
    # print(label, explanation)  
    # returntext = '{\n"claim": "' +  claim + '",\n"rating": "' + label + '",\n"factcheck": "' + explanation.replace('"', '').replace("'", '') + '"\n}'  
    # print(returntext)
    # return returntext
    return veracityPrediction_(claim, qa_pairs)
    
# print(folk("The default rate for college students has grown from 40 percent 10 years ago to about 50 percent today, and perhaps as many as 800,000 young Ohioans are facing default on their student loans.."))
'{\n"claim": "The default rate for college students has grown from 40 percent 10 years ago to about 50 percent today, and perhaps as many as 800,000 young Ohioans are facing default on their student loans..",\n"rating": "NOT_SUPPORTED",\n"factcheck": "The default rate for college students has not grown from 40 percent 10 years ago to about 50 percent today. The default rate for students from the lowest 25% of income-earners went into default at least once 12 years after entering repayment in 2003 was 41%. Among Black bachelors degree-completers in 2007-2008, about 34% had defaulted on a student loan at least once in the 10 years after graduation.\nAlso, it is not true that 800,000 young Ohioans are facing default on their student loans. In fact, 1 million Ohioans applied for student loan forgiveness and nearly 8,000 Ohioans had their student debt erased in February 2024."\n}'