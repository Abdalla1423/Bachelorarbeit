import pandas as pd
from type_definitions import PF_ENUM
from type_definitions import MODELS
from models.models import askModel
import ast
import os

nei_forms = ['nei', 'inconclusive', 'unverified', 'unkown', 'unverifiable', 'mixed', 'partially supported', 'not enough information', 'not enough info', 'neither', 'not_enough_information', 'insufficient']

def calculate_F1(strategies, model):
    results_list = []
    
    for strategy in strategies:
        
        file_path = f'results_new_dataset_cleaned/{model}/{strategy}_{model}.xlsx'
        df = pd.read_excel(file_path)

        # Convert all veracity columns to lowercase to handle inconsistencies
        df['Original Veracity'] = df['Original Veracity'].astype(str).str.lower()
        df['Determined Veracity'] = df['Determined Veracity'].astype(str).str.lower()

        TP = 0  # True Positives (predicted True, actually True)
        TN = 0  # True Negatives (predicted False, actually False)
        FP = 0  # False Positives (predicted True, actually False)
        FN = 0  # False Negatives (predicted False, actually True)
        NEIT = 0 # Num of NEI for true cases
        NEIF = 0 # Num of NEI for true cases

        for index, row in df.iterrows():
            original = row['Original Veracity']
            predicted = row['Determined Veracity']

            if predicted in nei_forms:
                if original == 'true':
                    NEIT += 1
                else:
                    NEIF += 1
            if original == 'true' and predicted == 'true':
                TP += 1
            elif original == 'false' and predicted == 'false':
                TN += 1
            elif original == 'false' and (predicted == 'true' or predicted in nei_forms):
                FP += 1
            elif original == 'true' and (predicted == 'false' or predicted in nei_forms):
                FN += 1

        # Calculate Precision, Recall, and F1 Score for True class
        precision_true = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall_true = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_true = 2 * (precision_true * recall_true) / (precision_true + recall_true) if (precision_true + recall_true) > 0 else 0

        # Calculate Precision, Recall, and F1 Score for False class
        precision_false = TN / (TN + FN) if (TN + FN) > 0 else 0
        recall_false = TN / (TN + FP) if (TN + FP) > 0 else 0
        f1_false = 2 * (precision_false * recall_false) / (precision_false + recall_false) if (precision_false + recall_false) > 0 else 0

        # Calculate Macro F1 Score
        macro_f1 = (f1_true + f1_false) / 2

        # Append the results for the current file to the results list
        # results_list.append({
        #     "Strategy": strategy,
        #     "True Positives (TP)": TP,
        #     "True Negatives (TN)": TN,
        #     "False Positives (FP)": FP,
        #     "False Negatives (FN)": FN,
        #     "NEI(True)": NEIT,
        #     "NEI(False)": NEIF,
        #     "Precision (True)": precision_true,
        #     "Recall (True)": recall_true,
        #     "F1 Score (True)": f1_true,
        #     "Precision (False)": precision_false,
        #     "Recall (False)": recall_false,
        #     "F1 Score (False)": f1_false,
        #     "Macro F1 Score": macro_f1,
        #     "Absolut Score": (TP + TN)/100,
        # })

        results_list.append({
            "Strategy": strategy,
            "F1 Score (True)": f1_true,
            "F1 Score (False)": f1_false,
            "NEI(True)": NEIT,
            "NEI(False)": NEIF,
            "Macro F1 Score": macro_f1
        })

    results_df = pd.DataFrame(results_list)

    output_file = f'results_{model}.xlsx'
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")

def calculate_proxy_based_F1(strategies, model):
    results_list = []
    
    for strategy in strategies:
        
        file_path = f'results_averitec_snippet/{model}/{strategy}_{model}_AVERITEC.xlsx'
        df = pd.read_excel(file_path)

        # Convert all veracity columns to lowercase to handle inconsistencies
        df['Original Veracity'] = df['Original Veracity'].astype(str).str.lower()
        df['Determined Veracity'] = df['Determined Veracity'].astype(str).str.lower()

        # Initialize counts for True Positives, True Negatives, False Positives, and False Negatives
        TP = 0  # True Positives (predicted True, actually True)
        TN = 0  # True Negatives (predicted False, actually False)
        FP = 0  # False Positives (predicted True, actually False)
        FN = 0  # False Negatives (predicted False, actually True)
        NEIT = 0 # Num of NEI for true cases
        NEIF = 0 # Num of NEI for true cases

        # Iterate through each row and count the true/false positives and negatives
        for index, row in df.iterrows():
            original = row['Original Veracity']
            predicted = row['Determined Veracity']

            if predicted in nei_forms:
                if original == 'supported':
                    NEIT += 1
                else:
                    NEIF += 1
            if original == 'supported' and predicted == 'supported':
                TP += 1
            elif original == 'refuted' and predicted == 'refuted':
                TN += 1
            elif original == 'refuted' and (predicted == 'supported' or predicted in nei_forms):
                FP += 1
            elif original == 'supported' and (predicted == 'refuted' or predicted in nei_forms):
                FN += 1


        # Calculate Precision, Recall, and F1 Score for True class
        precision_true = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall_true = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_true = 2 * (precision_true * recall_true) / (precision_true + recall_true) if (precision_true + recall_true) > 0 else 0

        # Calculate Precision, Recall, and F1 Score for False class
        precision_false = TN / (TN + FN) if (TN + FN) > 0 else 0
        recall_false = TN / (TN + FP) if (TN + FP) > 0 else 0
        f1_false = 2 * (precision_false * recall_false) / (precision_false + recall_false) if (precision_false + recall_false) > 0 else 0

        # Calculate Macro F1 Score
        macro_f1 = (f1_true + f1_false) / 2
        # Calculate Accuracy
        accuracy = (TP + TN) / (TP + FP + TN + FN)

        # Append the results for the current file to the results list
        # results_list.append({
        #     "Strategy": strategy,
        #     "True Positives (TP)": TP,
        #     "True Negatives (TN)": TN,
        #     "False Positives (FP)": FP,
        #     "False Negatives (FN)": FN,
        #     "NEI(True)": NEIT,
        #     "NEI(False)": NEIF,
        #     "Precision (True)": precision_true,
        #     "Recall (True)": recall_true,
        #     "F1 Score (True)": f1_true,
        #     "Precision (False)": precision_false,
        #     "Recall (False)": recall_false,
        #     "F1 Score (False)": f1_false,
        #     "Macro F1 Score": macro_f1,
        #     "Absolut Score": (TP + TN)/100,
        # })

        results_list.append({
            "Strategy": strategy,
            "F1 Score (Supported)": f1_true,
            "F1 Score (Refuted)": f1_false,
            "NEI(Supported)": NEIT,
            "NEI(Refuted)": NEIF,
            "Macro F1 Score": macro_f1,
            "Accuracy": accuracy,
        })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    output_file = f'results_averitec_snippet/{model}/results_proxy_based_{model}.xlsx'
    # Write the DataFrame to an Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")

def flattenGoldEvidence(evidences):
    evidences = ast.literal_eval(evidences)
    goldEvidence = ''
    for evidence in evidences:
        goldEvidence += evidence["question"] + ' '
        for answer_obj in evidence["answers"]:
            goldEvidence += answer_obj["answer"] + ' '
    return goldEvidence

def flattenRetrievedEvidence(evidences):
    evidences = ast.literal_eval(evidences)
    retrievedEvidence = ''
    for question, infos in evidences:
        if '?' in question:
            retrievedEvidence += question + ' '
        for info, _ in infos:
            retrievedEvidence += info
    return retrievedEvidence

def calculate_ref_based_F1(strategies, model):
    # Depending on how you get your data or claims, you might already have it in a DataFrame
    # or read it from a master file, etc. 
    # For demonstration, let's say we are going to read each Excel file (one per strategy).
    
    for strategy in strategies:
        file_path = f'results_averitec_snippet/{model}/{strategy}_{model}_AVERITEC.xlsx'
        
        # 1) Read existing file or create an empty DataFrame
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            # Create a DataFrame with the columns you expect 
            # (including columns for your metrics if you want them to exist upfront)
            df = pd.DataFrame(columns=[
                "Statement", 
                "Gold Evidence", 
                "Retrieved Information", 
                "Precision", 
                "Recall", 
                "F1"
            ])
        
        # 2) Iterate over rows in df. If you generate or have new statements somewhere else,
        #    you can adapt the logic to merge them in. 
        for index, row in df.iterrows():
            
            # OPTIONAL: Skip reprocessing any row that already has valid metrics
            #           or if it's marked as processed in some column.
            #           For example, if "Precision" is not NaN, we skip.
            if not pd.isna(row.get("Precision", float("nan"))) and row["Precision"] != -1:
                # print(f'Statement already processed. Skipping: "{row["Statement"]}"')
                continue
            
            # 3) Compute metrics for the row
            claim = row["Statement"]
            facts_count_predicted_evidence = 0
            facts_count_reference_evidence = 0
            if row["Retrieved Information"] == '[]':
                predicted = [] 
                support_predicted_evidence = -1
                support_reference_evidence = -1
            else:
                predicted = flattenRetrievedEvidence(row["Retrieved Information"])
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
            
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            # 4) Update the row in DataFrame
            df.loc[index, "Precision"] = precision
            df.loc[index, "Recall"] = recall
            df.loc[index, "F1"] = f1

            # 5) Save immediately after processing each row (partial save)
            #    This ensures your progress is stored if the script is interrupted.
            df.to_excel(file_path, index=False)

            print(f'Iteration {index+1}: Results appended and saved for statement "{claim}"')

        print(f'All statements processed for strategy "{strategy}" with model "{model}".')

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
    print(prompt, "\n", "\n", "\n", "\n")
    result = askModel(prompt)
    # print(result)
    try:
        result_obj = ast.literal_eval(result)
    except:
        return 1, -1, 1, -1


    return result_obj["facts count predicted evidence"], result_obj["support predicted evidence"], result_obj["facts count reference evidence"], result_obj["support reference evidence"]

def calculate_average_ref_based_f1(strategies, model):
    # Create an empty list to store the results for each file
    results_list = []
    
    # Iterate over each file in the array of file paths
    for strategy in strategies:
        
        file_path = f'results_averitec_snippet/{model}/{strategy}_{model}_AVERITEC.xlsx'
        # Load the Excel file
        df = pd.read_excel(file_path)


        F1_SUM = 0
        STATEMENT_COUNT = 0

        # Iterate through each row and count the true/false positives and negatives
        for index, row in df.iterrows():
            retrieved_information= row['Retrieved Information']
            if retrieved_information != '[]':
                F1_SUM += row['F1']
                STATEMENT_COUNT += 1

        AVG_F1 = F1_SUM/STATEMENT_COUNT

        results_list.append({
            "Strategy": strategy,
            "Average Ref F1": AVG_F1,
        })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    output_file = f'results_averitec_snippet/{model}/results_ref_based_based_{model}.xlsx'
    # Write the DataFrame to an Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")

def calculate_averitec_score(strategies, model):
    # Create an empty list to store the results for each file
    results_list = []
    
    # Iterate over each file in the array of file paths
    for strategy in strategies:
        
        file_path = f'results_averitec_snippet/{model}/{strategy}_{model}_AVERITEC.xlsx'
        # Load the Excel file
        df = pd.read_excel(file_path)

        df['Original Veracity'] = df['Original Veracity'].astype(str).str.lower()
        df['Determined Veracity'] = df['Determined Veracity'].astype(str).str.lower()


        CORRECT_LABELS = 0
        STATEMENT_COUNT = 0
        AVERITEC_SCORE = 0

        # Iterate through each row and count the true/false positives and negatives
        for index, row in df.iterrows():
            retrieved_information= row['Retrieved Information']
            gold_label = row['Original Veracity']
            predicted_label = row['Determined Veracity']
            recall_score = row['Recall']
            if retrieved_information != '[]':
                if gold_label == predicted_label and recall_score >= 0.25:
                    CORRECT_LABELS += 1
                STATEMENT_COUNT += 1
        print(strategy, CORRECT_LABELS, STATEMENT_COUNT)
        AVERITEC_SCORE = CORRECT_LABELS/STATEMENT_COUNT

        results_list.append({
            "Strategy": strategy,
            "Averitec score": AVERITEC_SCORE,
        })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    output_file = f'results_averitec_snippet/{model}/averitec_score_{model}_hiss.xlsx'
    # Write the DataFrame to an Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")

strategies = [PF_ENUM.KEYWORD.value, PF_ENUM.RARR.value, PF_ENUM.HISS.value, PF_ENUM.RAGAR.value]
calculate_averitec_score(strategies, MODELS.LLAMA_8B.value)
calculate_averitec_score(strategies, MODELS.GPT_4.value)
