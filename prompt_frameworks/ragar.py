# https://www.youtube.com/watch?v=JtZgVN84cN8

from models.models import askModel
from retriever.retriever import retrieve
import ast
import re

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
  6: Create a pointed factcheck question
  for the claim.
  Return only a python list containing the
  question and no other text.
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
- rating: choose among true, half-true and false,
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format and no other characters''')
  
def COTVeracityPrediction(claim, qa_pairs):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with question-answer pairs regarding the following claim: {claim}
Question-Answer Pairs:
{qa_pairs}
Based strictly on the main claim, and the question-answers provided (ignoring questions regarding image if they
dont have an answer), you will provide:
rating: The rating for claim should be one of "supported" if and only if the Question Answer Pairs specifically
support the claim, "refuted" if and only if the Question Answer Pairs specifically refutes the claim or
"failed": if there is not enough information to answer the claim appropriately.
Is the claim: {claim} "supported", "refuted"
or "failed" according to the available questions and answers?
Lets think step by step.''')
  
def verificationQuestion(claim, factcheck):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with the fact-check regarding the given claim
Claim: {claim}
Fact-Checked Response: {factcheck}
You are to generate verification questions.
A verification question is defined as a question that seeks to directly confirm whether a point made in the factchecked response is true or false.
Your task is the following:
1. Read the entire fact-check.
2. Identify overall points mentioned in the factcheck.
3. Create pointed verification questions by rephrasing the point verbatim as a Yes/No question for the overall
points mentioned in the fact-check.
4. The question must seek to gain answers in case of missing information suggested in the fact-check.
5. You must stick only to the overall points mentioned in the fact-check, do not create questions for unnecessary
extra information.
Instruction: You are not allowed to use the word "claim" or "statement". Instead if you want to refer the
claim/statement, you should point out the exact issue in the claim/statement that you are phrasing your question around.
Return only a python list containing the question and nothing else.''')

def correctionCheck(claim, factcheck, corrections):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with a factcheck and its correction qa pairs regarding the following claim: {claim}
Original FactCheck:
{factcheck}
Correction QA: {corrections}
Based strictly on the main claim, the original factcheck and the question-answers provided (ignoring questions
regarding image if they dont have
an answer), you will:
- If the corrections contain information that differs from the original factcheck, then create a new factchech
based on the corrected information and explain whether this changes the veracity of the original claim.
- If the corrections do not contain any new factcheck information. then simply return the original factcheck back.''')
  

  

  

def multiCoRAG(claim):
  questions = initialQuestion(claim)
  # print("initialQuestions: ", questions)
  # questions_list = questions.split('\n')
  # questions_list = [question[2:] for question in questions_list]
  # print(questions_list)
  questions_list = extract_questions(questions.replace('"', ""))
  qa_pairs = []
  for question in questions_list:
    qa_pairs += singleCoRag(claim, question)
  # print("total question_answer pairs: ", qa_pairs)
  prediction = veracityPrediction(claim, qa_pairs)
  # verificationQuestions = verificationQuestion(claim, prediction)
  # corrected_questions_list = ast.literal_eval(verificationQuestions)
  # corrected_qa_pairs = answerCorrectedQA(corrected_questions_list)
  # corrected_prediction = correctionCheck(claim, prediction, corrected_qa_pairs)
  return prediction

def answerCorrectedQA(corrected_questions_list):
  qa_pairs = []
  for question in corrected_questions_list:
    answer = retrieve(question)
    qa_pairs += (question, answer)
  return qa_pairs


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
    if followUpNeededAnswer == "No" or followUpNeededAnswer == "No.":
      followUpNeeded = True
      question = followupQuestion(claim, qa_pairs)
      # print("Follow Question: ", question)
    else:
      followUpNeeded = False
    counter += 1

  # print(qa_pairs)
  return qa_pairs
  
# print(multiCoRAG("State lawmakers are spending taxpayer money for parking that billionaire Arthur Blank could build while paying some state employees so little they are on food stamps."))

def extract_questions(questions):

  # Step 1: Replace the single quotes at the start of the list or after commas with double quotes
  fixed_string = re.sub(r"(?<=\[)'|(?<=, )'", '"', questions)

  # Step 2: Replace the single quotes before commas with double quotes
  fixed_string = re.sub(r"'(?=,)", '"', fixed_string)

  # Step 3: Replace the final single quote before the closing bracket with a double quote
  fixed_string = re.sub(r"'(?=])", '"', fixed_string)

  # Convert the fixed string to a list using ast.literal_eval
  output_list = ast.literal_eval(fixed_string)

  # Print the result
  return output_list




