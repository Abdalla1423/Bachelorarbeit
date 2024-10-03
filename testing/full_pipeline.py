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

matching_logic = {
    'true': ['mostly-true', 'true'],
    'half-true': ['mostly-true', 'half-true'],
    'false': ['barely-true', 'false', 'pants-fire'],
    'supported': ['mostly-true', 'true'],
    'refuted': ['barely-true', 'false', 'pants-fire'],
    'unsupported': ['barely-true', 'false', 'pants-fire'],
    'partially supported': ['mostly-true', 'half-true'],
    'unverifiable': ['barely-true', 'false', 'pants-fire'],
    'unverified': ['barely-true', 'false', 'pants-fire'],
    'not checkable': ['barely-true', 'false', 'pants-fire'],
    'mostly false': ['barely-true', 'false', 'pants-fire'],
}

NUM_OF_STATEMENTS = 100

def evaluate(claim: str, pf, name = ''):
    statement = name + " says " + claim
    verdict_str = pf_dict[pf](statement)
    try:
        verdict = ast.literal_eval(verdict_str)
    except:
        print("SHITTY FORM")
        print(verdict_str)
        return 'incorrect form', ''
    print(verdict_str)
    veracity = verdict["rating"]
    explanation = verdict['factcheck']
    return veracity, explanation

def preprocess():
    # Load the sampled data
    sampled_data_file = 'politifact_datasets/cleaned_statements.xlsx'
    # sampled_data_file = 'politifact_datasets/sampled_statements.xlsx'
    sampled_data = pd.read_excel(sampled_data_file)
    # Select only the first 5 statements
    sampled_data = sampled_data.head(NUM_OF_STATEMENTS)
    # Extract the part of the statement after the colon
    sampled_data['Statement'] = sampled_data['Statement'].apply(lambda x: x.split(':', 1)[-1].strip() if ':' in x else x)
    sampled_data.rename(columns={'Veracity': 'Original Veracity'}, inplace=True)
    return sampled_data


# Function to evaluate and save results for each strategy
# def evaluate_strategies(sampled_data, strategy):
#     # Apply the evaluate function to each statement
#     # sampled_data['Determined Veracity'] = sampled_data.apply(lambda row: evaluate(row['Statement'], strategy, row['Name']), axis=1)
#     # sampled_data['Determined Veracity'] = sampled_data['Statement'].apply(lambda x: evaluate(x, strategy))

#     determined_veracity = []
#     information = []
#     explanations = []

#     start_time = time.time()
#     # Iterate over each row in the DataFrame
#     for index, row in sampled_data.iterrows():
#         # Call the evaluate function with the required arguments and append the result to the list
#         result, exp = evaluate(row['Statement'], strategy, row['Name'])
#         information.append(retrieved_information[:])
#         explanations.append(exp)
#         determined_veracity.append(result)
#         retrieved_information.clear()
#         time.sleep(5)
#     end_time = time.time()
#     # Assign the results back to the 'Determined Veracity' column
#     sampled_data['Determined Veracity'] = determined_veracity
#     sampled_data['Retrieved Information'] = information
#     sampled_data['Explanation'] = explanations
#     elapsed_time = end_time - start_time
    
 
#     # Create a new DataFrame with the required columns
#     evaluated_data = sampled_data[['Statement', 'Name', 'Original Veracity', 'Determined Veracity','Explanation', 'Retrieved Information']].copy()
#     # Save the output to a new file
#     output_file_path = f'{strategy}_claimant_nei_content_new_ret_scrape_nonamekw.xlsx'
#     evaluated_data.to_excel(output_file_path, index=False)
#     print(f'Results saved for strategy "{strategy}" in file: {output_file_path}')
#     print(f'Elapsed time: {elapsed_time} s')
#     return evaluated_data

# Function to evaluate and save results for each strategy

import os
from openpyxl import load_workbook

import os

# Function to evaluate and save results for each strategy iteratively
def evaluate_strategies(sampled_data, strategy):
    # Define the output file path
    output_file_path = f'{strategy}.xlsx'
    
    # Check if the file already exists
    if os.path.exists(output_file_path):
        # Load the existing data
        evaluated_data = pd.read_excel(output_file_path)
    else:
        # Create an empty DataFrame if file doesn't exist
        evaluated_data = pd.DataFrame(columns=['Statement', 'Name', 'Original Veracity', 'Determined Veracity', 'Explanation', 'Retrieved Information'])
    
    determined_veracity = []
    explanations = []

    start_time = time.time()
    
    # Iterate over each row in the DataFrame
    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        if not evaluated_data[evaluated_data['Statement'] == row['Statement']].empty:
            print(f"Statement {row['Statement']} already processed. Skipping.")
            continue
        
        # Call the evaluate function with the required arguments and append the result to the list
        result, exp = evaluate(row['Statement'], strategy, row['Name'])
        explanations.append(exp)
        determined_veracity.append(result)
        
        
        # Create a temporary DataFrame for this iteration
        temp_df = pd.DataFrame({
            'Statement': [row['Statement']],
            'Name': [row['Name']],
            'Original Veracity': [row['Original Veracity']],
            'Determined Veracity': [result],
            'Explanation': [exp],
            'Retrieved Information': [retrieved_information[:]]
        })
        retrieved_information.clear()
        
        # Append the new row to the evaluated_data DataFrame
        evaluated_data = pd.concat([evaluated_data, temp_df], ignore_index=True)
        
        # Save the updated DataFrame to the output file after each iteration
        evaluated_data.to_excel(output_file_path, index=False)
        print(f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

        # Pause to avoid overwhelming the server or hitting rate limits
        time.sleep(5)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f'All statements processed for strategy "{strategy}". Elapsed time: {elapsed_time} s')
    return evaluated_data



def evaluate_and_determine_score(strategy):
    sampled_data = preprocess()
    evaluated_data = evaluate_strategies(sampled_data, strategy)
    score = determine_score(evaluated_data)
    print(f'Score: {score}/{NUM_OF_STATEMENTS}')
    return score

def determine_score(evaluated_data):
    # Convert both columns to lowercase for case-insensitive comparison
    evaluated_data['Original Veracity'] = evaluated_data['Original Veracity'].astype(str).str.lower()
    evaluated_data['Determined Veracity'] = evaluated_data['Determined Veracity'].astype(str).str.lower()

    # Check for matches
    evaluated_data['Match'] = evaluated_data.apply(
        lambda row: row['Original Veracity'] in matching_logic.get(row['Determined Veracity'], []),
        axis=1
    )

    # Count the number of matches
    matches_count = evaluated_data['Match'].sum()
    
    return matches_count

def determine_score_file(file_path = "results_new_dataset/LLAMA_7B/RARR_plain_claimant_nei.xlsx"):
    df = pd.read_excel(file_path)
    matches_count = determine_score(df)
    return matches_count
#Hiss incorrect form needs correction
# print(determine_score_file())
# evaluate_and_determine_score(PF_ENUM.BASELINE)
# evaluate_and_determine_score(PF_ENUM.KEYWORD)
# evaluate_and_determine_score(PF_ENUM.RARR)

evaluate_and_determine_score(PF_ENUM.RAGAR)
evaluate_and_determine_score(PF_ENUM.HISS)




# print(determine_score_file())
# print(evaluate_and_determine_score(PF_ENUM.RARR))
# print(evaluate_and_determine_score(PF_ENUM.RARR))
# print(evaluate_and_determine_score(PF_ENUM.BASELINE))
# print(evaluate_and_determine_score(PF_ENUM.KEYWORD))
# print(evaluate_and_determine_score(PF_ENUM.RARR))
# print(determine_score_file())
# print(evaluate_and_determine_score(PF_ENUM.RAGAR))


# print(evaluate_and_determine_score(PF_ENUM.BASELINE))
    

# Run the evaluation for all strategies
# evaluate_strategies(sampled_data, PF_ENUM.BASELINE)
# evaluate_strategies(sampled_data, PF_ENUM.KEYWORD)
# evaluate_strategies(sampled_data, PF_ENUM.HISS)
# rarr 54 7$
# base 60 5$
# HISS 57 20$
# keyword 59 6$


# Base 59
# Keyword 65
# RARR 62


# 
# base
# statement: 69
# claim: 62
# rarr
# statement: 74
# claim: 59

# rarr with nei
# 54
# rarr without nei
# 52

