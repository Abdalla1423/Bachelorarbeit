from testing.type_definitions import prompt_frameworks_fn, model_map, prompt_frameworks_map, retriever_map
import ast
import pandas as pd
from retriever.info import retrieved_information
import time
import os
import argparse
from models.models import setModel
from retriever.retriever import set_retriever


NUM_OF_STATEMENTS = 100

#   This function uses the specified prompt framework (pf) to determine the veracity
#   of a given claim. If a 'name' is provided, it prepends that name to the claim text
#   before sending it to the framework. It then attempts to parse the result as JSON
#   to extract a 'label' and an 'explanation'.


def evaluate(claim: str, pf, name=''):
    if name:
        statement = name + " says " + claim
        verdict_str = prompt_frameworks_fn[pf](statement)
    else:
        verdict_str = prompt_frameworks_fn[pf](claim)
    try:
        verdict = ast.literal_eval(verdict_str)
    except:
        return 'incorrect form', ''
    veracity = verdict["label"]
    explanation = verdict["explanation"]
    return veracity, explanation


def preprocess_averitec():
    sampled_data_file = 'data/averitec_100.xlsx'
    sampled_data = pd.read_excel(sampled_data_file)
    sampled_data = sampled_data.head(NUM_OF_STATEMENTS)
    sampled_data.rename(columns={'Label': 'Original Veracity'}, inplace=True)
    sampled_data.rename(columns={'Claim': 'Statement'}, inplace=True)
    return sampled_data


def flattenGoldEvidence(evidences):
    evidences = ast.literal_eval(evidences)
    goldEvidence = ''
    for evidence in evidences:
        goldEvidence += evidence["question"] + ' '
        for answer_obj in evidence["answers"]:
            goldEvidence += answer_obj["answer"] + ' '
    return goldEvidence


def flattenRetrievedEvidence(evidences):
    retrievedEvidence = ''
    for question, infos in evidences:
        if '?' in question:
            retrievedEvidence += question + ' '
        for info, _ in infos:
            retrievedEvidence += info
    return retrievedEvidence

#   Runs a specific evidence retrieval / prompt framework strategy against the AVERITEC
#   dataset. It processes each statement in the dataset, skipping those already completed
#   in an existing output file. The results are continuously written to an Excel file.


def evaluate_strategy(strategy, model):
    sampled_data = preprocess_averitec()
    output_file_path = f'{strategy}_{model}_AVERITEC.xlsx'

    if os.path.exists(output_file_path):
        evaluated_data = pd.read_excel(output_file_path)
    else:
        evaluated_data = pd.DataFrame(columns=[
                                      'Statement', 'Original Veracity', 'Determined Veracity', 'Explanation', 'Retrieved Information'])

    determined_veracity = []
    explanations = []

    start_time = time.time()

    for index, row in sampled_data.iterrows():
        # Check if the current statement has already been processed (to avoid duplicates)
        filtered_data = evaluated_data[evaluated_data['Statement']
                                       == row['Statement']]
        if not filtered_data.empty:
            print(f"Statement {row['Statement']} already processed. Skipping.")
            continue
        if 'Name' in sampled_data.columns:
            name = row['Name']
        else:
            name = ''
        result, exp = evaluate(row['Statement'], strategy, name)
        explanations.append(exp)
        determined_veracity.append(result)

        temp_df = pd.DataFrame({
            'Statement': [row['Statement']],
            'Original Veracity': [row['Original Veracity']],
            'Determined Veracity': [result],
            'Explanation': [exp],
            'Retrieved Information': [retrieved_information[:]],
            'Gold Evidence': [row['Questions']]
        })
        retrieved_information.clear()

        evaluated_data = pd.concat(
            [evaluated_data, temp_df], ignore_index=True)

        evaluated_data.to_excel(output_file_path, index=False)
        print(
            f'Iteration {index+1}: Results appended and saved for statement "{row["Statement"]}"')

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(
        f'All statements processed for strategy "{strategy}" and dataset "AVERITEC". Elapsed time: {elapsed_time} s')
    return evaluated_data

#   The main entry point for running the full pipeline:
#   1. Parses CLI arguments to choose a model and one or more strategies.
#   2. Sets the selected model and retriever globally.
#   3. Calls 'evaluate_strategy' for each chosen strategy.


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        choices=["gpt4", "llama8b"],
        required=True,
        help="Which model to use? Options: 'gpt4' or 'llama8b'. Example usage: python main.py --model gpt4"
    )
    parser.add_argument(
        "--strategy",
        nargs="+",
        choices=["baseline", "rarr", "keyword", "corag", "hiss"],
        required=True,
        help="Which strategy (or strategies) to use? One or more allowed."
    )
    args = parser.parse_args()

    chosen_model = model_map[args.model]
    setModel(chosen_model)

    chosen_retriever = retriever_map["serper"]
    set_retriever(chosen_retriever)

    chosen_strategies = [prompt_frameworks_map[strategy]
                         for strategy in args.strategy]
    for chosen_strategy in chosen_strategies:
        evaluate_strategy(chosen_strategy, chosen_model)


if __name__ == "__main__":
    main()
