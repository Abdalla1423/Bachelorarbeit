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
import json


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
}

def evaluate(claim, pf):
    verdict_str = pf_dict[pf](claim)
    print(verdict_str)
    verdict = ast.literal_eval(verdict_str)
    print(verdict)
    veracity = verdict["rating"]
    return veracity

def preprocess():
    # Load the sampled data
    sampled_data_file = 'sampled_statements.xlsx'
    sampled_data = pd.read_excel(sampled_data_file)

    # Select only the first 5 statements
    sampled_data = sampled_data.head(20)

    # Extract the part of the statement after the colon
    sampled_data['Statement'] = sampled_data['Statement'].apply(lambda x: x.split(':', 1)[-1].strip() if ':' in x else x)
    return sampled_data


# Function to evaluate and save results for each strategy
def evaluate_strategies(sampled_data, strategy):
    # Apply the evaluate function to each statement
    sampled_data['Determined Veracity'] = sampled_data['Statement'].apply(lambda x: evaluate(x, strategy))
    print(sampled_data)
    
    # Create a new DataFrame with the required columns
    evaluated_data = sampled_data[['Statement', 'Determined Veracity']].copy()
    evaluated_data['Original Veracity'] = sampled_data['Veracity']
    print(evaluated_data)
    # Save the output to a new file
    output_file_path = f'evaluated_data_{strategy}_llama7b.xlsx'
    evaluated_data.to_excel(output_file_path, index=False)
    print(f'Results saved for strategy "{strategy}" in file: {output_file_path}')
    return evaluated_data

def evaluate_and_determine_score(strategy):
    sampled_data = preprocess()
    evaluated_data = evaluate_strategies(sampled_data, strategy)
    score = determine_score(evaluated_data)
    return score

def determine_score(evaluated_data):
    # Convert both columns to lowercase for case-insensitive comparison
    evaluated_data['Original Veracity'] = evaluated_data['Original Veracity'].str.lower()
    evaluated_data['Determined Veracity'] = evaluated_data['Determined Veracity'].str.lower()
    # print(evaluated_data)

    # Check for matches
    evaluated_data['Match'] = evaluated_data.apply(
        lambda row: row['Original Veracity'] in matching_logic.get(row['Determined Veracity'], []),
        axis=1
    )
    
    print(evaluated_data)

    # Count the number of matches
    matches_count = evaluated_data['Match'].sum()

    return matches_count

def determine_score_file(file_path = "./evaluated_data_PF_ENUM.RAGAR.xlsx"):
    df = pd.read_excel(file_path)
    matches_count = determine_score(df)
    return matches_count

# print(determine_score_file())


print(evaluate_and_determine_score(PF_ENUM.RARR))
    

# Run the evaluation for all strategies
# evaluate_strategies(sampled_data, PF_ENUM.BASELINE)
# evaluate_strategies(sampled_data, PF_ENUM.KEYWORD)
# evaluate_strategies(sampled_data, PF_ENUM.HISS)


