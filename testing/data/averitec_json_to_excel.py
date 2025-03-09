import json
import pandas as pd

def json_to_excel(json_file, excel_file):
    # Load JSON data from file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare a list to hold flattened rows
    rows = []

    for item in data:
        # Flatten main fields
        row = {
            'Claim': item.get('claim'),
            'Required Reannotation': item.get('required_reannotation'),
            'Label': item.get('label'),
            'Justification': item.get('justification'),
            'Claim Date': item.get('claim_date'),
            'Speaker': item.get('speaker'),
            'Original Claim URL': item.get('original_claim_url'),
            'Fact Checking Article': item.get('fact_checking_article'),
            'Reporting Source': item.get('reporting_source'),
            'Location ISO Code': item.get('location_ISO_code'),
            'Claim Types': item.get('claim_types', []),
            'Fact Checking Strategies': item.get('fact_checking_strategies', []),
            'Questions': item.get('questions', [])
        }

        # Add the row to the list
        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Write to Excel
    df.to_excel(excel_file, index=False, engine='openpyxl')

def sample_claims(input_excel, output_excel):
    # Load the Excel file
    df = pd.read_excel(input_excel)

    # Sample 50 rows for each label
    supported_samples = df[df['Label'] == 'Supported'].sample(n=50, random_state=1)
    refuted_samples = df[df['Label'] == 'Refuted'].sample(n=50, random_state=1)

    # Combine samples
    sampled_df = pd.concat([supported_samples, refuted_samples])

    # Write to a new Excel file
    sampled_df.to_excel(output_excel, index=False, engine='openpyxl')

# Example usage
json_file = 'dev.json'  # Replace with the path to your JSON file
excel_file = 'averitec.xlsx'  # Replace with the desired output Excel file
sampled_excel_file = 'averitec_100.xlsx'  # Replace with the desired sampled output Excel file

# # Convert JSON to Excel
# json_to_excel(json_file, excel_file)

# Sample claims and write to a new Excel file
sample_claims(excel_file, sampled_excel_file)

print(f"Sampled claims have been saved to {sampled_excel_file}.")
