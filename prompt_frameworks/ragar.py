# https://www.youtube.com/watch?v=JtZgVN84cN8

from models.models import askModel
from retriever.retriever import retrieve
import ast
import re
import time
from prompt_frameworks.veracity_prediction import veracityPrediction

  
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
  4: You must not ask if the claim was actually
  made by the person. It is guaranteed that the 
  person made the claim.
  5: You must not ask for sources of data.
  You are only concerned with the questions.
  6: You are not allowed to use the word
  "claim". Instead, if you want to refer to
  the claim, you should point out the exact
  issue in the claim that you are phrasing
  your questions around.
  7: You must never ask for calculations or
  methodology.
  8: Create a pointed factcheck question
  for the claim.
  Return only a python list containing 
  the question in text format and no other characters.
  Don't include any types of quotation marks or apostroph in the question
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
It is guaranteed that the person made the claim.
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

  

def multiCoRAG(claim):
  questions = initialQuestion(claim)
  questions_list = ast.literal_eval(questions)
  # questions_list = extract_questions(questions.replace('"', ""))
  qa_pairs = []
  for question in questions_list:
    qa_pairs += singleCoRag(claim, question)
  # time.sleep(2)
  prediction = veracityPrediction(claim, qa_pairs)
  return prediction

def singleCoRag(claim, question):
  qa_pairs = []
  counter = 0
  followUpNeeded = True
  
  while counter < 6 and followUpNeeded:
    answer = retrieve(question)
    qa_pairs.append((question, answer))
    # time.sleep(2)
    followUpNeededAnswer = followupCheck(claim, qa_pairs)
    if followUpNeededAnswer == "No" or followUpNeededAnswer == "No.":
      followUpNeeded = True
      # time.sleep(2)
      question = followupQuestion(claim, qa_pairs)
    else:
      followUpNeeded = False
    counter += 1

  return qa_pairs
  

def extract_questions(questions):

  fixed_string = re.sub(r"(?<=\[)'|(?<=, )'", '"', questions)

  fixed_string = re.sub(r"'(?=,)", '"', fixed_string)

  fixed_string = re.sub(r"'(?=])", '"', fixed_string)

  match = re.search(r"\[(.*?)\]", fixed_string)

  output_list = ast.literal_eval(f"[{match.group(1)}]")

  return output_list
