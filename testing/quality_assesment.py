from datasets import Dataset 
from ragas.metrics import faithfulness
from ragas import evaluate
import os
import pandas as pd
from dotenv import load_dotenv
import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")

NUM_OF_STATEMENTS = 5

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


def compute_similarity(source_sentence, comparison_sentences):
    # Encode the source sentence and comparison sentences
    source_embedding = model.encode([source_sentence])
    comparison_embeddings = model.encode(comparison_sentences)

    # Compute cosine similarity between the source sentence and each comparison sentence
    similarities = cosine_similarity(source_embedding, comparison_embeddings)

    # Return the similarity scores (it's a 1xN matrix, so we extract the row)
    return similarities[0]

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
    output_file_path = f'{strategy}_Faithfulness.xlsx'
    
    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=['Statement', 'Formatted Statement', 'Name', 'Explanation', 'Retrieved Information', 'Faithfulness', 'Sentence Similarity'])

    
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
        sentence_similarity = 0
        if row['Retrieved Information']:
            score = evaluate(dataset,metrics=[faithfulness])
            res_df = score.to_pandas()
            faithfulness_score = res_df['faithfulness']
            sentence_similarity = compute_similarity(row['Statement'], row['Retrieved Information'])
        else:
            print("No retrieved information!")
        
        temp_df = pd.DataFrame({
            'Formatted Statement': [row['Formatted Statement']],
            'Statement': [row['Statement']],
            'Name': [row['Name']],
            'Explanation': [row['Explanation']],
            'Retrieved Information': [row['Retrieved Information']],
            'Faithfulness': faithfulness_score,
            'Sentence Similarity': sentence_similarity[0],
        })
        
        evaluated_data = pd.concat([evaluated_data, temp_df], ignore_index=True)
        
        evaluated_data.to_excel(output_file_path, index=False)
        print(f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

    
    print(f'All statements processed for strategy "{strategy}"')
    return evaluated_data

evaluate_strategies("RARR", "GPT_4")

