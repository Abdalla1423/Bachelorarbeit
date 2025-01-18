from type_definitions import pf_dict, PF_ENUM, MODELS
import ast
import pandas as pd
from retriever.info import retrieved_information
import time
import os




NUM_OF_STATEMENTS = 100

def evaluate(claim: str, pf, name = ''):
    statement = name + " says " + claim
    verdict_str = pf_dict[pf](statement)
    try:
        verdict = ast.literal_eval(verdict_str)
    except:
        print(verdict_str)
        print("INCORRECT FORM")
        return 'incorrect form', ''
    veracity = verdict["rating"]
    print(verdict)
    explanation = verdict['factcheck']
    return veracity, explanation

def preprocess():
    sampled_data_file = 'politifact_datasets/cleaned_statements.xlsx'
    sampled_data = pd.read_excel(sampled_data_file)
    sampled_data = sampled_data.head(NUM_OF_STATEMENTS)
    sampled_data['Statement'] = sampled_data['Statement'].apply(lambda x: x.split(':', 1)[-1].strip() if ':' in x else x)
    sampled_data.rename(columns={'Veracity': 'Original Veracity'}, inplace=True)
    return sampled_data



# Function to evaluate and save results for each strategy iteratively
def evaluate_strategies(strategy, model):
    sampled_data = preprocess()
    output_file_path = f'{strategy}_{model}.xlsx'
    
    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=['Statement', 'Name', 'Original Veracity', 'Determined Veracity', 'Explanation', 'Retrieved Information'])
    
    determined_veracity = []
    explanations = []

    start_time = time.time()
    
    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        # and filtered_data.iloc[0]["Determined Veracity"] != "incorrect form"
        filtered_data = evaluated_data[evaluated_data['Statement'] == row['Statement']]
        if not filtered_data.empty: 
            print(f"Statement {row['Statement']} already processed. Skipping.")
            continue
        
        result, exp = evaluate(row['Statement'], strategy, row['Name'])
        explanations.append(exp)
        determined_veracity.append(result)
        
        temp_df = pd.DataFrame({
            'Statement': [row['Statement']],
            'Name': [row['Name']],
            'Original Veracity': [row['Original Veracity']],
            'Determined Veracity': [result],
            'Explanation': [exp],
            'Retrieved Information': [retrieved_information[:]]
        })
        retrieved_information.clear()
        
        evaluated_data = pd.concat([evaluated_data, temp_df], ignore_index=True)
        
        evaluated_data.to_excel(output_file_path, index=False)
        print(f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

        # Pause to avoid overwhelming the server or hitting rate limits
        # time.sleep(5)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f'All statements processed for strategy "{strategy}". Elapsed time: {elapsed_time} s')
    return evaluated_data

# evaluate_strategies(PF_ENUM.BASELINE.value, MODELS.LLAMA_8B.value)
evaluate_strategies(PF_ENUM.KEYWORD.value, MODELS.LLAMA_8B.value)
evaluate_strategies(PF_ENUM.RARR.value, MODELS.LLAMA_8B.value)
evaluate_strategies(PF_ENUM.HISS.value, MODELS.LLAMA_8B.value)
evaluate_strategies(PF_ENUM.RAGAR.value, MODELS.LLAMA_8B.value)
