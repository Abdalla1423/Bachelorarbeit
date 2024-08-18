from models.models import askModel
from retriever.google_retriever import google_search


# prompt = ['''
# Claim: "Emerson Moser, who was Crayola’s top crayon molder for almost 40 years, was colorblind."
# A fact checker will decompose the claim into 4 subclaims that are easier to verify:
# 1.Emerson Moser was a crayon molder at Crayola.
# 2.Moser worked at Crayola for almost 40 years.
# 3.Moser was Crayola's top crayon molder.
# 4.Moser was colorblind.
# To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Is there any official record or documentation indicating that Emerson Moser worked as a crayon molder at Crayola?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: Yes.
# To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Are there any official records or documentation confirming Emerson Moser's length of employment at Crayola?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: Emerson Moser, who is retiring next week after 35 years, isn't colorblind in the sense that he can't see color at all. It's just that some ...
# To verify subclaim 3, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Are there credible sources or publications that mention Emerson Moser as Crayola's top crayon molder?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: Yes.
# To verify subclaim 4, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Are there any credible sources or records indicating that Emerson Moser was colorblind?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: Yes.
# Question: Was Emerson Moser's colorblindness only confusing for certain colors?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: Moser has had tritanomaly, a type of colorblindness that makes it difficult to distinguish between blue and green and between yellow and red.
# Based on the answers to these questions, it is clear that among pants-fire, false, barely-true, half-true, mostly-true, and true, the claim can be classified as mostly-true.

# Claim: "Bernie Sanders said 85 million Americans have no health insurance."
# A fact checker will not split the claim since the original claim is easier to verify.
# To verify the claim, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: How many Americans did Bernie Sanders claim had no health insurance?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: "We have 85 million Americans who have no health insurance," Sanders said Dec. 11 on CNN's State of the Union.
# Question: How did Bernie Sanders define "no health insurance"?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: Sanders spokesperson Mike Casca said the senator was referring to the number of uninsured and under-insured Americans and cited a report about those numbers for adults.
# Question: How many Americans were uninsured or under-insured according to the Commonwealth Fund survey?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: The Commonwealth Fund survey found that 43% of working-age adults 19 to 64, or about 85 million Americans, were uninsured or inadequately insured.
# Question: Is the statement "we have 85 million Americans who have no health insurance" partially accurate according to the information in the passage?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: Bernie Sanders omitted that his figure included people who either have no health insurance or are under-insured.
# Based on the answers to these questions, it is clear that among pants-fire, false, barely-true, half-true, mostly-true, and true, the claim is classified as half-true.

# Claim: "JAG charges Nancy Pelosi with treason and seditious conspiracy."
# A fact checker will decompose the claim into 2 subclaims that are easier to verify:
# 1. JAG has made a claim or accusation against Nancy Pelosi.
# 2. The specific charges or allegations made against Nancy Pelosi are treason and seditious conspiracy.
# To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Is it true that JAG has made a claim or accusation against Nancy Pelosi?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: There is no evidence to support this claim and a spokesperson for the U.S. Navy Judge Advocate General's Corps has stated that it is not true.
# To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
# Question: Is it true that the specific charges or allegations made against Nancy Pelosi are treason and seditious conspiracy?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: There is no evidence to support this claim.
# Question: Where is the source of the claim?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: Real Raw News, a disclaimer stating that it contains "humor, parody and satire" and has a history of publishing fictitious stories.
# Based on the answers to these questions, it is clear that among pants-fire, false, barely-true, half-true, mostly-true, and true, the claim is classified as pants-fire.

# Claim: "Cheri Beasley “backs tax hikes — even on families making under $75,000."
# A fact checker will decompose the claim into 2 subclaims that are easier to verify:
# 1.Cheri Beasley supports tax increases.
# 2.Cheri Beasley supports tax increases for families with an income under $75,000.
# To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she might raise each question and look for an answer:
# Question: Does Cheri Beasley support tax increases?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
# Answer: Beasley supports student loan bailouts for the wealthy.
# To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she might raise each question and look for an answer:
# Question: Does the ad accurately link Beasley's position on student loan debt forgiveness with her stance on tax hikes for families making under $75,000 per year?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: The ad makes a misleading connection between the two issues and does not accurately represent Beasley's position on tax hikes for families making under $75,000 per year.
# Question: Has Cheri Beasley ever advocated for tax hikes specifically on families making under $75,000?
# Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
# Answer: No evidence found that Cheri Beasley has explicitly advocated for such a tax hike.
# Based on the answers to these questions, it is clear that among pants-fire, false, barely-true, half-true, mostly-true, and true, the claim can be classified as barely-true.
# Claim: ''', '''A fact checker will''',
#  ]

# def promptf(claim, prompt, intermediate = "\nAnswer:", followup = "Intermediate Question", finalans= '\nBased on the answers to these questions, it is clear that among among pants-fire, false, barely-true, half-true, mostly-true, and true, the claim '):
#     cur_prompt = prompt[0] +  claim + " " + prompt[1]

#     # print(question, end ='')

#     ret_text = gpt4Ask(cur_prompt,stop=['Answer me ‘yes’ or ‘no’: No.'])
#     if 'Output:' in ret_text:
#       return cur_prompt + ret_text

    
#     # print("RET TEXT:    ", ret_text)
#     while 'Output:' not in ret_text:
#       cur_prompt += ret_text +'Answer me ‘yes’ or ‘no’: No.'
#       question = ret_text.split('\nTell me')[0].split('\n')[-1]
#       question = extract_question(ret_text)
#       # print('question')
#       # print(question)
#       # print('Answer:')
#       external_answer = ''.join(google_search(question))
#       # print('external_answer')
#       # print(external_answer)
#       cur_prompt += intermediate + ' ' + external_answer + '.\n' 
#       ret_text = gpt4Ask(cur_prompt, ['Answer me ‘yes’ or ‘no’: No.'])

#     cur_prompt += finalans
#     cur_prompt += claim
#     cur_prompt += 'can be classified as'
#     ret_text = gpt4Ask(cur_prompt, ['\n'])

#     return cur_prompt + " " +  ret_text
 
basePrompt = ['''
Claim: "Emerson Moser, who was Crayola’s top crayon molder for almost 40 years, was colorblind."
A fact checker will decompose the claim into 4 subclaims that are easier to verify:
1.Emerson Moser was a crayon molder at Crayola.
2.Moser worked at Crayola for almost 40 years.
3.Moser was Crayola's top crayon molder.
4.Moser was colorblind.
To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Is there any official record or documentation indicating that Emerson Moser worked as a crayon molder at Crayola?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: Yes.
To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Are there any official records or documentation confirming Emerson Moser's length of employment at Crayola?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: Emerson Moser, who is retiring next week after 35 years, isn't colorblind in the sense that he can't see color at all. It's just that some ...
To verify subclaim 3, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Are there credible sources or publications that mention Emerson Moser as Crayola's top crayon molder?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: Yes.
To verify subclaim 4, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Are there any credible sources or records indicating that Emerson Moser was colorblind?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: Yes.
Question: Was Emerson Moser's colorblindness only confusing for certain colors?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: Moser has had tritanomaly, a type of colorblindness that makes it difficult to distinguish between blue and green and between yellow and red.

Output: 
{
  "claim": "Emerson Moser, who was Crayola’s top crayon molder for almost 40 years, was colorblind.",
  "rating": "supported",
  "factcheck": "The claim that Emerson Moser was Crayola’s top crayon molder for almost 40 years and was colorblind is supported by the information provided. There is official documentation indicating that Emerson Moser worked as a crayon molder at Crayola, and credible sources confirm that he was Crayola’s top crayon molder. Although the documentation suggests that Moser worked at Crayola for 35 years rather than 'almost 40 years,' this minor discrepancy does not significantly undermine the overall claim. Additionally, it is confirmed that Moser had tritanomaly, a type of colorblindness, which supports the final part of the claim."
}

Claim: "Bernie Sanders said 85 million Americans have no health insurance."
A fact checker will not split the claim since the original claim is easier to verify.
To verify the claim, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: How many Americans did Bernie Sanders claim had no health insurance?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: "We have 85 million Americans who have no health insurance," Sanders said Dec. 11 on CNN's State of the Union.
Question: How did Bernie Sanders define "no health insurance"?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: Sanders spokesperson Mike Casca said the senator was referring to the number of uninsured and under-insured Americans and cited a report about those numbers for adults.
Question: How many Americans were uninsured or under-insured according to the Commonwealth Fund survey?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: The Commonwealth Fund survey found that 43% of working-age adults 19 to 64, or about 85 million Americans, were uninsured or inadequately insured.
Question: Is the statement "we have 85 million Americans who have no health insurance" partially accurate according to the information in the passage?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: Bernie Sanders omitted that his figure included people who either have no health insurance or are under-insured.

Output: 
{
  "claim": "Bernie Sanders said 85 million Americans have no health insurance.",
  "rating": "refuted",
  "factcheck": "The claim made by Bernie Sanders that 85 million Americans have no health insurance is refuted by the information provided. While Sanders did mention the figure of 85 million Americans, it was in reference to the total number of uninsured and under-insured individuals, not just those without any health insurance. The Commonwealth Fund survey cited by Sanders' spokesperson confirms that the 85 million figure includes both uninsured and inadequately insured individuals, making Sanders' statement misleading."
}

Claim: "JAG charges Nancy Pelosi with treason and seditious conspiracy."
A fact checker will decompose the claim into 2 subclaims that are easier to verify:
1. JAG has made a claim or accusation against Nancy Pelosi.
2. The specific charges or allegations made against Nancy Pelosi are treason and seditious conspiracy.
To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Is it true that JAG has made a claim or accusation against Nancy Pelosi?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: There is no evidence to support this claim and a spokesperson for the U.S. Navy Judge Advocate General's Corps has stated that it is not true.
To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she raise each question and look for an answer:
Question: Is it true that the specific charges or allegations made against Nancy Pelosi are treason and seditious conspiracy?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: There is no evidence to support this claim.
Question: Where is the source of the claim?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: Real Raw News, a disclaimer stating that it contains "humor, parody and satire" and has a history of publishing fictitious stories.

Output:
{
  "claim": "JAG charges Nancy Pelosi with treason and seditious conspiracy.",
  "rating": "refuted",
  "factcheck": "The claim that JAG (Judge Advocate General's Corps) has charged Nancy Pelosi with treason and seditious conspiracy is refuted. There is no evidence to support this claim, and a spokesperson for the U.S. Navy Judge Advocate General's Corps has explicitly stated that it is not true. Furthermore, the source of the claim, Real Raw News, is a website known for publishing fictitious stories under the guise of satire, further discrediting the claim."
}

Claim: "Cheri Beasley “backs tax hikes — even on families making under $75,000."
A fact checker will decompose the claim into 2 subclaims that are easier to verify:
1.Cheri Beasley supports tax increases.
2.Cheri Beasley supports tax increases for families with an income under $75,000.
To verify subclaim 1, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she might raise each question and look for an answer:
Question: Does Cheri Beasley support tax increases?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: Yes.
Answer: Beasley supports student loan bailouts for the wealthy.
To verify subclaim 2, a fact-checker will go through a step-by-step process to ask and answer a series of questions relevant to its factuality. Here are the specific steps he/she might raise each question and look for an answer:
Question: Does the ad accurately link Beasley's position on student loan debt forgiveness with her stance on tax hikes for families making under $75,000 per year?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: The ad makes a misleading connection between the two issues and does not accurately represent Beasley's position on tax hikes for families making under $75,000 per year.
Question: Has Cheri Beasley ever advocated for tax hikes specifically on families making under $75,000?
Tell me if you are confident to answer the question or not. Answer me ‘yes’ or ‘no’: No.
Answer: No evidence found that Cheri Beasley has explicitly advocated for such a tax hike.

Output:
{
  "claim": "Cheri Beasley “backs tax hikes — even on families making under $75,000.",
  "rating": "refuted",
  "factcheck": "The claim that Cheri Beasley backs tax hikes even on families making under $75,000 is refuted. While Beasley supports student loan forgiveness, the connection made between this position and tax hikes for families earning under $75,000 is misleading. There is no evidence to suggest that Beasley has explicitly advocated for such tax hikes. The claim appears to misrepresent Beasley's stance on taxation by inaccurately linking it to her support for student loan forgiveness."
}

Claim: ''', '''A fact checker will''',
 ]
 
def hiss(claim):
    cur_prompt = basePrompt[0] +  claim + " " + basePrompt[1]
    ret_text = askModel(cur_prompt,stop=['Answer me ‘yes’ or ‘no’: No.'])
    if 'Output:' in ret_text:
      fullPrompt = cur_prompt + ret_text
      return ret_text.split('Output:')[1]
    
    while 'Output:' not in ret_text:
      cur_prompt += ret_text +'Answer me ‘yes’ or ‘no’: No.'
      question = ret_text.split('\nTell me')[0].split('\n')[-1]
      question = extract_question(ret_text)
      print('question')
      print(question)
      print('Answer:')
      external_answer = ''.join(google_search(question))
      print('external_answer')
      print(external_answer)
      cur_prompt += "\nAnswer:" + ' ' + external_answer + '.\n' 
      ret_text = askModel(cur_prompt, 'Answer me ‘yes’ or ‘no’: No.')

    fullPrompt = cur_prompt + ret_text
    return ret_text.split('Output:')[1]


def extract_question(generated):
    generated = generated.split('Question: ')[-1].split('Answer')[0]
    return generated



# print(hiss("Today President Biden died."))