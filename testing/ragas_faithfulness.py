from datasets import Dataset 
from ragas.metrics import FaithulnesswithHHEM
from ragas.metrics import faithfulness
from ragas import evaluate
import os
import pandas as pd
from dotenv import load_dotenv
import ast

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")

NUM_OF_STATEMENTS = 100

faithfulness_with_hhem = FaithulnesswithHHEM()

def clean_context(context):
    return [info[0] for _, infos in context for info in infos]
   
def preprocess(strategy, model):
    file_path = f'results_new_dataset/{model}/{strategy}_{model}.xlsx'
    sampled_data = pd.read_excel(file_path)
    sampled_data = sampled_data.head(NUM_OF_STATEMENTS)
    sampled_data['Statement'] = sampled_data.apply(lambda row: f'Is this statement made by {row["Name"]} true: {row["Statement"]}', axis=1)
    sampled_data['Retrieved Information'] = sampled_data['Retrieved Information'].apply(lambda context: clean_context(ast.literal_eval(context)))
    return sampled_data


def evaluate_strategies(strategy, model):
    sampled_data = preprocess(strategy, model)
    output_file_path = f'{strategy}_Faithfulness.xlsx'
    
    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=['Statement', 'Name', 'Explanation', 'Retrieved Information', 'Faithfulness'])

    
    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        if not evaluated_data[evaluated_data['Statement'] == row['Statement']].empty:
            print(f"Statement {row['Statement']} already processed. Skipping.")
            continue
        
        data_samples = {
            'question': [row['Statement']],
            'answer': [row['Explanation']],
            'contexts' : [row['Retrieved Information']],
        }
        
        dataset = Dataset.from_dict(data_samples)       
        faithfulness_score = 0
        if row['Retrieved Information']:
            score = evaluate(dataset,metrics=[faithfulness])
            res_df = score.to_pandas()
            faithfulness_score = res_df['faithfulness']
        else:
            print("No retrieved information!")
        
        temp_df = pd.DataFrame({
            'Statement': [row['Statement']],
            'Name': [row['Name']],
            'Explanation': [row['Explanation']],
            'Retrieved Information': [row['Retrieved Information']],
            'Faithfulness': faithfulness_score
        })
        
        evaluated_data = pd.concat([evaluated_data, temp_df], ignore_index=True)
        
        evaluated_data.to_excel(output_file_path, index=False)
        print(f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

    
    print(f'All statements processed for strategy "{strategy}"')
    return evaluated_data

evaluate_strategies("RARR", "GPT_4")

