import pandas as pd

def process_files_to_excel(strategies, model):
    # Create an empty list to store the results for each file
    results_list = []
    
    # Iterate over each file in the array of file paths
    for strategy in strategies:
        
        file_path = f'results_new_dataset/{model}/{strategy}_{model}.xlsx'
        # Load the Excel file
        df = pd.read_excel(file_path)

        # Convert all veracity columns to lowercase to handle inconsistencies
        df['Original Veracity'] = df['Original Veracity'].astype(str).str.lower()
        df['Determined Veracity'] = df['Determined Veracity'].astype(str).str.lower()

        # Initialize counts for True Positives, True Negatives, False Positives, and False Negatives
        TP = 0  # True Positives (predicted True, actually True)
        TN = 0  # True Negatives (predicted False, actually False)
        FP = 0  # False Positives (predicted True, actually False)
        FN = 0  # False Negatives (predicted False, actually True)

        # Iterate through each row and count the true/false positives and negatives
        for index, row in df.iterrows():
            original = row['Original Veracity']
            predicted = row['Determined Veracity']

            if original == 'true' and predicted == 'true':
                TP += 1
            elif original == 'false' and predicted == 'false':
                TN += 1
            elif original == 'false' and (predicted == 'true' or predicted == 'nei'):
                FP += 1
            elif original == 'true' and (predicted == 'false' or predicted == 'nei'):
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
        results_list.append({
            "Strategy": strategy,
            "True Positives (TP)": TP,
            "True Negatives (TN)": TN,
            "False Positives (FP)": FP,
            "False Negatives (FN)": FN,
            "Precision (True)": precision_true,
            "Recall (True)": recall_true,
            "F1 Score (True)": f1_true,
            "Precision (False)": precision_false,
            "Recall (False)": recall_false,
            "F1 Score (False)": f1_false,
            "Macro F1 Score": macro_f1,
            "Absolut Score": (TP + TN)/100,
        })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    output_file = f'results_{model}.xlsx'
    # Write the DataFrame to an Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results successfully written to {output_file}")

strategies = ["BASELINE", "KEYWORD", "RARR","HISS", "RAGAR"]
model = "Llama_8B"

process_files_to_excel(strategies, model)
