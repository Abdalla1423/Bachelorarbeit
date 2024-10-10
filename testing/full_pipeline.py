from prompt_frameworks.ragar import multiCoRAG
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from prompt_frameworks.baseline import base
from prompt_frameworks.baseline import base_fewshot
from prompt_frameworks.keywords import keyword
from prompt_frameworks.direct import direct
from prompt_frameworks.folk_cot import folk_cot
from prompt_frameworks.folk import folk
from enum import Enum
import ast
import pandas as pd
from retriever.info import retrieved_information
import time
import os


class PF_ENUM(Enum):
    RAGAR = 'RAGAR'
    HISS = 'HISS'
    RARR = 'RARR'
    BASELINE = 'BASELINE'
    BASELINE_FEWSHOT = 'BASELINE_FEWSHOT'
    KEYWORD = 'KEYWORD'
    DIRECT = 'DIRECT'
    FOLK_COT = 'FOLK_COT'
    FOLK = 'FOLK'

pf_dict = {PF_ENUM.RAGAR: multiCoRAG, PF_ENUM.HISS: hiss, 
           PF_ENUM.RARR: rarr, PF_ENUM.BASELINE: base, 
           PF_ENUM.BASELINE_FEWSHOT: base_fewshot,
           PF_ENUM.KEYWORD: keyword, PF_ENUM.DIRECT: direct,
           PF_ENUM.FOLK_COT: folk_cot, PF_ENUM.FOLK: folk}

NUM_OF_STATEMENTS = 1

def evaluate(claim: str, pf, name = ''):
    statement = name + " says " + claim
    verdict_str = pf_dict[pf](statement)
    try:
        verdict = ast.literal_eval(verdict_str)
    except:
        print("INCORRECT FORM")
        print(verdict_str)
        return 'incorrect form', ''
    print(verdict_str)
    veracity = verdict["rating"]
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
def evaluate_strategies( strategy):
    sampled_data = preprocess()
    output_file_path = f'{strategy}.xlsx'
    
    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=['Statement', 'Name', 'Original Veracity', 'Determined Veracity', 'Explanation', 'Retrieved Information'])
    
    determined_veracity = []
    explanations = []

    start_time = time.time()
    
    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        if not evaluated_data[evaluated_data['Statement'] == row['Statement']].empty:
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
        time.sleep(5)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f'All statements processed for strategy "{strategy}". Elapsed time: {elapsed_time} s')
    return evaluated_data


