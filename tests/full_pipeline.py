from prompt_frameworks.ragar import multiCoRAG
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from enum import Enum
import ast
import pandas as pd

class PF_ENUM(Enum):
    RAGAR = 'RAGAR'
    HISS = 'HISS'
    RARR = 'RARR'

pf_dict = {PF_ENUM.RAGAR: multiCoRAG, PF_ENUM.HISS: hiss, PF_ENUM.RARR: rarr}

def evaluate(claim, pf):
    verdict_str = pf_dict[pf](claim)
    verdict = ast.literal_eval(verdict_str)
    print(verdict)
    veracity = verdict["rating"]
    return veracity

# Load the sampled data
sampled_data_file = 'sampled_statements.xlsx'
sampled_data = pd.read_excel(sampled_data_file)

# Select only the first 5 statements
sampled_data = sampled_data.head(5)

# Extract the part of the statement after the colon
sampled_data['Statement'] = sampled_data['Statement'].apply(lambda x: x.split(':', 1)[-1].strip() if ':' in x else x)


# Function to evaluate and save results for each strategy
def evaluate_strategies(sampled_data, strategy):
    # Apply the evaluate function to each statement
    sampled_data['Determined Veracity'] = sampled_data['Statement'].apply(lambda x: evaluate(x, strategy))
    
    # Create a new DataFrame with the required columns
    evaluated_data = sampled_data[['Statement', 'Determined Veracity']].copy()
    evaluated_data['Original Veracity'] = sampled_data['Veracity']
    
    # Save the output to a new file
    output_file_path = f'evaluated_data_{strategy}.xlsx'
    evaluated_data.to_excel(output_file_path, index=False)
    print(f'Results saved for strategy "{strategy}" in file: {output_file_path}')

# Run the evaluation for all strategies
evaluate_strategies(sampled_data, PF_ENUM.RARR)
