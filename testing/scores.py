import pandas as pd
from testing.type_definitions import prompt_frameworks_map
from testing.type_definitions import model_map
from models.models import askModel, setModel
import ast
import os
import argparse
from testing.full_pipeline import flattenGoldEvidence, flattenRetrievedEvidence

#   For each strategy associated with the given model, this function opens the
#   corresponding results file (an Excel spreadsheet) and calculates precision, recall,
#   and F1 for each statement. The metrics are based on how closely the retrieved
#   evidence matches the reference evidence (gold standard), by comparing the atomic facts
#   their atomic facts.


def calculate_ref_based_precision_recall_f1(model, prompt_frameworks):
    for prompt_framework in prompt_frameworks:
        file_path = f'results_averitec_snippet/{model}/{prompt_framework}_{model}_AVERITEC.xlsx'

        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            df = pd.DataFrame(columns=[
                "Statement",
                "Gold Evidence",
                "Retrieved Information",
                "Precision",
                "Recall",
                "F1"
            ])

        for index, row in df.iterrows():

            if not pd.isna(row.get("Precision", float("nan"))) and row["Precision"] != -1:
                continue

            claim = row["Statement"]
            facts_count_predicted_evidence = 0
            facts_count_reference_evidence = 0
            if row["Retrieved Information"] == '[]':
                predicted = []
                support_predicted_evidence = -1
                support_reference_evidence = -1
            else:
                predicted = flattenRetrievedEvidence(ast.literal_eval(
                    row["Retrieved Information"]))
                gold = flattenGoldEvidence(row["Gold Evidence"])

                (facts_count_predicted_evidence, support_predicted_evidence,
                 facts_count_reference_evidence, support_reference_evidence
                 ) = split_and_compare(claim, predicted, gold)

            precision = 0.0
            recall = 0.0
            if facts_count_predicted_evidence > 0:
                precision = support_predicted_evidence / facts_count_predicted_evidence
            if facts_count_reference_evidence > 0:
                recall = support_reference_evidence / facts_count_reference_evidence

            f1 = 2 * (precision * recall) / (precision +
                                             recall) if (precision + recall) > 0 else 0

            df.loc[index, "Precision"] = precision
            df.loc[index, "Recall"] = recall
            df.loc[index, "F1"] = f1

            df.to_excel(file_path, index=False)

            print(
                f'Iteration {index+1}: Results appended and saved for statement "{claim}"')

        print(
            f'All statements processed for strategy "{prompt_framework}" with model "{model}".')


def split_and_compare(claim, predicted_evidence, gold_evidence):
    prompt = f''' You will get as input a claim, a reference evidence and a predicted evidence.
Please verify the correctness of the predicted evidence by comparing it to the reference evidence, following these steps:
1. Break down the PREDICTED evidence in independent facts. Each fact should be a separate sentence.
3. Evaluate each fact individually: is the fact supported by the REFERENCE evidence? Do not use additional sources or background
knowledge.
4. Next, break down the REFERENCE evidence in independent facts. Each fact should be a separate sentence.
5. Evaluate each fact individually: is the fact supported by the PREDICTED evidence? Do not use additional sources or background
knowledge.
5. Finally summarise (1.) how many predicted facts are supported by the reference evidence, (2.) how many reference facts are
supported by the predicted evidence.
Generate the output in form of a json as shown in the examples below!
----- Examples:
                      
Claim: Mukesh Ambani, richest man in Asia had surgery for pancreatic cancer at Sloan Kettering, New York, US cancer speciality
hospital on October 30, 2020.
                      
Reference evidence: When was the photograph taken of Mukesh Ambani, the richest man in Asia, on the Facebook post claiming he
had been diagnosed with pancreatic cancer and had undergone surgery? The photograph was taken on September 5, 2020. When
was a video filmed of Mukesh Ambani at the virtual launch of NK Singh's book Portrait of Power? The video was filmed on October
19, 2020. What date was the Facebook post which confirmed Mukesh Ambani had lost 30 kgs, been diagnosed with pancreatic
cancer and had had liver transplant surgery? The Facebook post was dated November 2, 2020. Where was Mukesh's photo of him
supposedly recieving surgery actually taken? It was taken by Manushree Vijayvergiya who shared her experience of meeting Mukesh
and Isha Ambani in a cafe in Liechtenstein.
                      
Predicted evidence: Who was the man who allegedly threatened Mukhesh Ambani: Question answer: What was his name and where
was he from? New Delhi: The man had allegedly called on the HN Reliance Foundation Hospital and issued threats to Mukesh
Ambani in filthy language. What are the predictions by Chiragh Darwalla for Ambanis? Astrology Predictions for Mukesh Ambani by
Astrologer Chirag Daruwalla. Mukesh Ambani is an Indian industrialist and the chairman and managing director of Reliance Industries.
What happened to Mukhesh Ambanis net worth? Nov 2, 2020 Mumbai: Mukesh Ambani, Asia's richest man, lost as much as $7 billion
from his networth as Reliance Industries Ltd.'s shares tumbled to the lowest price in more than three months following a.

Output: {{
"facts in predicted evidence": "1. A man allegedly called on the HN Reliance Foundation Hospital and issued threats to
Mukesh Ambani. 2. Astrologer Chirag Daruwalla issues predictions for Mukesh Ambani. 3. Mukesh Ambani is an Indian
industrialist. 4. Mukesh Ambani is the chairman and managing director of Reliance Industries. 5. Mukesh Ambani is Asia's richest
man. 6. Mukesh Ambani lost $7 billion from his networth as Reliance Industries Ltd.'s shares tumbled to the lowest price in more
than three months.",
 "fact check predicted evidence": "1. A man allegedly called on the HN Reliance Foundation Hospital and issued threats to
Mukesh Ambani. The reference evidence does not mention anything about a man calling and threatening Mukesh Ambani. Not
enough information. 2. Astrologer Chirag Daruwalla issues predictions for Mukesh Ambani. The reference evidence does not
mention anything about an Astrologer giving predictions about Mukesh Ambani's future. Not enough information. 3. Mukesh
Ambani is an Indian industrialist. The reference evidence does not mention that Mukesh Ambani is an Indian industrialist. Not
enough information. 4. Mukesh Ambani is the chairman and managing director of Reliance Industries. The reference evidence
does not mention that Mukesh Ambani is the managing director of Reliance Industries. Not enough information. 5. Mukesh
Ambani is Asia's richest man. The fact 'Mukesh Ambani is Asia's richest man' is supported by the reference evidence. 6. Mukesh
Ambani lost $7 billion from his networth as Reliance Industries Ltd.'s shares tumbled to the lowest price in more than three
months. The reference evidence does not mention that Mukesh Ambani lost money or why he lost it. Not enough information.",
"facts count predicted evidence": 6,
"support predicted evidence": 1,
"facts in reference evidence": "1. Mukhesh Aambi is the richest man in Asia. 2. On September 5, 2020 a photograph of
Mukesh Ambani was taken claiming he had been diagnosed with pancreatic cancer and had undergone surgery. 3. On October
19, 2020 a video of Mukesh Ambani was filmed at the virtual launch of NK Singh's book. 4. On November 2, 2020 a Facebook
post was posted confirming that Mukesh Ambani had lost 30 kgs, been diagnosed with pancreatic cancer and had had liver
transplant surgery. 5. A photo of Mukhesh Ambani supposedly recieving surgery actually taken in Liechtenstein.",
"fact check reference evidence": "1. Mukhesh Aambi is the richest man in Asia. The predicted evidence mentions that
Mukhesh Ambani is Asia's richest man, this fact is hence supported. 2. On September 5, 2020 a photograph of Mukesh Ambani
was taken claiming he had been diagnosed with pancreatic cancer and had undergone surgery. The predicted evidence does
not mention anything about Mukhesh Ambani's cancer diagnosis or surgery. Not enough information. 3. On October 19, 2020 a
video of Mukesh Ambani was filmed at the virtual launch of NK Singh's book. Predicted evidence does not mention Ambani
attending any book launch. Not enough information. 4. On November 2, 2020 a Facebook post was posted confirming that
Mukesh Ambani had lost 30 kgs, been diagnosed with pancreatic cancer and had had liver transplant surgery. The predicted
evidence does not mention any of this. Not enough information. 5. A photo of Mukhesh Ambani supposedly recieving surgery
was actually taken in Liechtenstein. The predicted evdience does not mention anything about a survey or Ambani being in
Liechtenstein. Not enough information.",
"facts count reference evidence": 5,
"support reference evidence": 1
}}

Claim: {claim}

Reference evidence: {gold_evidence}

Predicted evidence: {predicted_evidence}

Output:
                      
'''
    result = askModel(prompt)
    try:
        result_obj = ast.literal_eval(result)
    except:
        return 1, -1, 1, -1

    return result_obj["facts count predicted evidence"], result_obj["support predicted evidence"], result_obj["facts count reference evidence"], result_obj["support reference evidence"]


#   Computes two main metrics for each strategy:
#   1. Accuracy: Fraction of statements for which the predicted label matches the gold label.
#   2. AVERITEC score: Fraction of statements for which both the label is correct AND recall >= 0.44


def calculate_averitec_and_accuracy(model, prompt_frameworks):
    results_list = []

    for prompt_framework in prompt_frameworks:

        file_path = f'results_averitec_snippet/{model}/{prompt_framework}_{model}_AVERITEC.xlsx'
        df = pd.read_excel(file_path)

        df['Original Veracity'] = df['Original Veracity'].astype(
            str).str.lower()
        df['Determined Veracity'] = df['Determined Veracity'].astype(
            str).str.lower()

        CORRECT_LABELS = 0
        CORRECT_LABELS_AND_EVIDENCES = 0
        STATEMENT_COUNT = 0
        AVERITEC_SCORE = 0
        ACCURACY = 0

        for index, row in df.iterrows():
            gold_label = row['Original Veracity']
            predicted_label = row['Determined Veracity']
            if gold_label == predicted_label:
                CORRECT_LABELS += 1
                if row['Recall'] >= 0.44:
                    CORRECT_LABELS_AND_EVIDENCES += 1
            STATEMENT_COUNT += 1
        AVERITEC_SCORE = CORRECT_LABELS_AND_EVIDENCES/STATEMENT_COUNT
        ACCURACY = CORRECT_LABELS/STATEMENT_COUNT

        results_list.append({
            "Strategy": prompt_framework,
            "Accuracy": ACCURACY,
            "Averitec score": AVERITEC_SCORE,
        })

    results_df = pd.DataFrame(results_list)

    output_file = f'results_averitec_snippet/{model}/scores_{model}.xlsx'
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")


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

    chosen_strategies = [prompt_frameworks_map[strategy]
                         for strategy in args.strategy]

    calculate_ref_based_precision_recall_f1(chosen_model, chosen_strategies)
    calculate_averitec_and_accuracy(chosen_model, chosen_strategies)


if __name__ == "__main__":
    main()
