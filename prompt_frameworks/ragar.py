# https://www.youtube.com/watch?v=JtZgVN84cN8

from models.models import askModel
from retriever.retriever import retrieve
import ast

def initialQuestions(claim):
  return askModel(f'''
  You are an expert fact-checker given an unverified claim that needs to be explored.
  Claim: {claim}
  Country: United States of America
  You follow these Instructions:
  1: You understand the entire claim.
  2: You will make sure that the questions
  are specific and focus on one aspect of
  the claim (focus on one topic, should
  detail where, who, and what) and is very,
  very short.
  3: You should not appeal to video
  evidence nor ask for calculations or
  methodology.
  3: You must not ask for sources of data.
  You are only concerned with the questions.
  4: You are not allowed to use the word
  "claim". Instead, if you want to refer to
  the claim, you should point out the exact
  issue in the claim that you are phrasing
  your questions around.
  5: You must never ask for calculations or
  methodology.
  6: Create pointed factcheck questions
  for the claim.
  Return only a python list containing the
  questions and nothing else.
      ''')
  
def initialQuestion(claim):
  return askModel(f'''
  You are an expert fact-checker given an unverified claim that needs to be explored.
  Claim: {claim}
  Country: United States of America
  You follow these Instructions:
  1: You understand the entire claim.
  2: You will make sure that the question
  is specific and focuses on one aspect of
  the claim (focus on one topic, should
  detail where, who, and what) and is very,
  very short.
  3: You should not appeal to video
  evidence nor ask for calculations or
  methodology.
  3: You must not ask for sources of data.
  You are only concerned with the questions.
  4: You are not allowed to use the word
  "claim". Instead, if you want to refer to
  the claim, you should point out the exact
  issue in the claim that you are phrasing
  your questions around.
  5: You must never ask for calculations or
  methodology.
  6: Create pointed factcheck questions
  for the claim.
  Return only a python list containing the
  question and nothing else.
      ''')

def followupQuestion(claim, qa_pairs):
  return askModel(f'''You are given an unverified statement and
question-answer pairs regarding the claim
that needs to be explored. You follow
these steps:
Claim: {claim}
Question-Answer Pairs:
{qa_pairs}
Country: United States of America
Your task is to ask a followup question
to regarding the claim specifically based
on the question answer pairs.
Never ask for sources or publishing.
The follow-up question must be
descriptive, specific to the claim, and
very short, brief, and concise.
The follow-up question should not appeal
to video evidence nor ask for
calculations or methodology.
The followup question
should not be
seeking to answer a previously asked
question. It can however attempt to
improve the question.
You are not allowed to use the word
"claim" or "statement". Instead if you
want to refer the claim/statement, you
should point out the exact issue
in the
claim/statement that you are phrasing
your question around.
Reply only with the followup question and
nothing else.''')

def followupCheck(claim, qa_pairs):
  return askModel(f'''You are an expert fact-checker given an
unverified claim and question-answer
pairs regarding the claim that needs to
be explored. You follow these steps:
Claim: {claim}
Question-Answer Pairs:
{qa_pairs}
Are you satisfied with the questions
asked and do you have enough
information to answer the claim?
If the answer to any of these questions
is "Yes", then reply only with "Yes"
or else answer, "No"''')

def veracityPrediction(claim, qa_pairs):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with question-answer pairs regarding the following claim: {claim}
These are the provided questions and relevant answers to the question to verify the claim:
< {qa_pairs}>
Based strictly on the main claim and the question-answers provided (ignoring questions regarding image if they
dont have an answer), You have to provide:
- claim: the original claim,
- rating: the rating for claim should be "supported" if and only if the Question Answer Pairs specifically
support the claim, "refuted" if and only if the Question Answer Pairs specifically refute the claim or "failed":
if there is not enough information to answer the claim appropriately.
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format''')
  

def multiCoRAG(claim):
  questions = initialQuestions(claim)
  # print("initialQuestions: ", questions)
  # questions_list = questions.split('\n')
  # questions_list = [question[2:] for question in questions_list]
  # print(questions_list)
  questions_list = ast.literal_eval(questions)
  qa_pairs = []
  for question in questions_list:
    qa_pairs += singleCoRag(claim, question)
  # print("total question_answer pairs: ", qa_pairs)
  return veracityPrediction(claim, qa_pairs)
  

def singleCoRag(claim, question):
  # print("next question: ", question)
  qa_pairs = []
  counter = 0
  followUpNeeded = True
  
  while counter < 6 and followUpNeeded:
    answer = retrieve(question)
    # print("answer: ", answer)
    qa_pairs.append((question, answer))
    followUpNeededAnswer = followupCheck(claim, qa_pairs)
    # print("Follow up needed: ", followUpNeededAnswer)
    if followUpNeededAnswer == "Yes.":
      followUpNeeded = True
      question = followupQuestion(claim, qa_pairs)
      # print("Follow Question: ", question)
    else:
      followUpNeeded = False
    counter += 1

  # print(qa_pairs)
  return qa_pairs
  
# print(multiCoRAG("Today President Biden died."))