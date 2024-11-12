from datasets import Dataset 
from ragas.metrics import faithfulness
from ragas import evaluate
import os
import pandas as pd
from dotenv import load_dotenv
import ast
from sentence_transformers import SentenceTransformer, util
from models.models import askModel

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")

NUM_OF_STATEMENTS = 10

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


def compute_relevance(statement, information):
    ranking = rank_sentences(statement, information)
    answer = askModel('''Your task is to judge the relevance of a series of information snippets based on a given statement that needs to be verified. For each information snippet you must return verdict as 1 if the information snippet is relevant to verify the given statement or 0 if the information snippet is not be relevant to verify the given statement.

The output should be a well-formatted JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output JSON schema:
{"type": "array", "items": {"$ref": "#/definitions/SnippetFaithfulnessAnswer"}, "definitions": {"SnippetFaithfulnessAnswer": {"title": "SnippetFaithfulnessAnswer", "type": "object", "properties": {"information snippet": {"title": "information snippet", "description": "the original information snippet, word-by-word", "type": "string"}, "reason": {"title": "Reason", "description": "the reason of the verdict", "type": "string"}, "verdict": {"title": "Verdict", "description": "the verdict(0/1) of the faithfulness.", "type": "integer"}}, "required": ["information snippet", "reason", "verdict"]}}}


Do not return any preamble or explanations, return only a pure JSON string surrounded by triple backticks (
).

Examples:

information snippets:
["Albert Einstein was a genius", "Barack Obama is 54."]
statement: "Go look at other countries that went through exactly this, started to reopen, and then they saw the infection rate go back up again."
answer:
[{"information snippet": "Albert Einstein was a genius.", "reason": "The context and statement are unrelated", "verdict": 0}, {"information snippet": "Barack Obama is 54.", "reason": "The context and statement are unrelated", "verdict": 0}]
information snippets:
["Go look at other countries that went through exactly this, started to reopen, and then they saw the infection rate go back up again," he said.There have been reports of increased infection rates in some countries that reopened.Our ruling\nCuomo didn’t say that all countries had increased infections after they reopened, and he also didn’t say explicitly that reopening caused the increase in the statement we fact-checked"]
statement: "Go look at other countries that went through exactly this, started to reopen, and then they saw the infection rate go back up again."
answer:
[{"information snippet": "Go look at other countries that went through exactly this, started to reopen, and then they saw the infection rate go back up again," he said.There have been reports of increased infection rates in some countries that reopened.Our ruling\nCuomo didn’t say that all countries had increased infections after they reopened, and he also didn’t say explicitly that reopening caused the increase in the statement we fact-checked", "reason": "The snippet is directly referencing the statement.", "verdict": 1}]
Your actual task:'''
+
f'''
context: {ranking[:3]}
statement: {statement}
answer: 
''')    
    
    answer_arr = ast.literal_eval(answer[3:-3])
    verdict_sum = sum([obj['verdict'] for obj in answer_arr])
    return verdict_sum/3

def rank_sentences(statement, information):
    query_embedding = model.encode(statement, convert_to_tensor=True)
    sentence_embeddings = model.encode(information, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)

    # Rank sentences based on the cosine similarity scores
    sentence_scores = list(zip(information, cosine_scores[0].cpu().numpy()))
    ranked_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    
    return [ranked_sentence[0] for ranked_sentence in ranked_sentences]

def clean_context(context):
    return [info[0] for _, infos in context for info in infos]
   
def preprocess(strategy, model):
    file_path = f'results_new_dataset/{model}/{strategy}_{model}.xlsx'
    sampled_data = pd.read_excel(file_path)
    sampled_data = sampled_data.head(NUM_OF_STATEMENTS)
    sampled_data['Formatted Statement'] = sampled_data.apply(lambda row: f'Is this statement made by {row["Name"]} true: {row["Statement"]}', axis=1)
    sampled_data['Retrieved Information'] = sampled_data['Retrieved Information'].apply(lambda context: clean_context(ast.literal_eval(context)))
    return sampled_data


def evaluate_strategies(strategy, model):
    sampled_data = preprocess(strategy, model)
    output_file_path = f'{strategy}_Relevance_2.xlsx'
    
    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=['Statement', 'Formatted Statement', 'Name', 'Determined Veracity', 'Explanation', 'Retrieved Information', 'Faithfulness', 'Relevance'])

    
    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        if not evaluated_data[evaluated_data['Formatted Statement'] == row['Formatted Statement']].empty:
            print(f"Statement {row['Formatted Statement']} already processed. Skipping.")
            continue
     
        data_samples = {
            'question': [row['Formatted Statement']],
            'answer': [row['Explanation']],
            'contexts' : [row['Retrieved Information']],
        }
        
        dataset = Dataset.from_dict(data_samples)       
        faithfulness_score = 0
        relevance_score = 0

        if row['Retrieved Information']:
            score = evaluate(dataset,metrics=[faithfulness])
            res_df = score.to_pandas()
            faithfulness_score = res_df['faithfulness']
            relevance_score = compute_relevance(row['Statement'], row['Retrieved Information'])
        else:
            print("No retrieved information!")
        
        temp_df = pd.DataFrame({
            'Formatted Statement': [row['Formatted Statement']],
            'Statement': [row['Statement']],
            'Name': [row['Name']],
            'Determined Veracity': [row['Determined Veracity']],
            'Explanation': [row['Explanation']],
            'Retrieved Information': [row['Retrieved Information']],
            'Faithfulness': faithfulness_score,
            'Relevance': relevance_score,
        })
        
        evaluated_data = pd.concat([evaluated_data, temp_df], ignore_index=True)
        
        evaluated_data.to_excel(output_file_path, index=False)
        print(f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

    
    print(f'All statements processed for strategy "{strategy}"')
    return evaluated_data

evaluate_strategies("RARR", "GPT_4")

