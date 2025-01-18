from models.models import askModel
from retriever.retriever import retrieve
import re
from prompt_frameworks.veracity_prediction import veracityPrediction

def question_generation(claim):
  questions = askModel(f'''
I will check things you said and ask questions. Follow the format and generate questions about the last claim!
It is guaranteed that the person made the claim, so focus only on the contents of the claim!
(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes. This
is to prevent a buildup of mucus. It's called the nasal cycle.
To verify it,
a) I googled: Does your nose switch between nostrils?
b) I googled: How often does your nostrils switch?
c) I googled: Why does your nostril switch?
d) I googled: What is nasal cycle?
(2) You said: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford's psychology building.
To verify it,
a) I googled: Where was Stanford Prison Experiment was conducted?
(3) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its adjacency
list. It is named after Vaclav Havel and Samih Hakimi.
To verify it,
a) I googled: What does Havel-Hakimi algorithm do?
b) I googled: Who are Havel-Hakimi algorithm named after?
(4) You said: "Time of My Life" is a song, by American singer-songwriter Bill Medley from the soundtrack of the 1987 film
Dirty Dancing. The song was produced by Michael Lloyd.
To verify it,
a) I googled: Who sings "Time of My Life"?
b) I googled: Who produced me some ty of tea
(5) You said: Kelvin Hopins was suspended from the Labor Party due to his membership in the Conservative Party.
To verify it,
a) I googled: Why was Kelvin Hopins suspended from Labor Party?
(6) You said: Social work is a profession that is based in the philosophical tradition of humanism. It is an intellectual
discipline that has its roots in the 1800s.
To verify it,
a) I googled: What philosophical tradition is social work based on?
b) I googled: what year does social work has its root in?
(7) You said: {claim}
To verify it:
     ''')
  
  return questions

def extract_questions(text):
    # Regular expression pattern to identify questions
    question_pattern = re.compile(r"[A-Za-z]\)\s*I googled:\s*(.*\?)")

    # Extracting all the questions
    questions = question_pattern.findall(text)
    
    return questions

def rarr(claim):
  generated_questions = question_generation(claim)
  extracted_questions = extract_questions(generated_questions)
  qa_pairs = []
  
  for question in extracted_questions:
    answer = retrieve(question)
    qa_pairs.append((question, answer))
  prediction = veracityPrediction(claim, qa_pairs)
  return prediction

