# Analyzing Evidence Retrieval in AFC

This repository contains tools for evaluating statements using various models and frameworks, calculating F1 MACRO scores, and assessing quality. Follow the setup and instructions below to get started.

## Setup

1. **Install Dependencies**  
   Download and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Keys**  
   Obtain the following API keys and store them in a `.env` file:
   - `OPENAI_API_KEY`
   - `SERP_API_KEY`

   optional:
    - `GOOGLE_API_KEY`
    - `GOOGLE_CSE_ID`

## Evaluation of Statements

1. **Set the Model**  
   Open `models/models.py` and specify the model you intend to use for evaluation.

2. **Choose Prompt Framework and Number of Statements**  
   - Navigate to the `full_pipeline.py` file in the `testing` folder.
   - Choose your desired prompt framework.
   - Set the number of statements to evaluate by adjusting `NUM_OF_STATEMENTS`.

3. **Run the Evaluation**  
   - Call the function `evaluate_strategies(prompt_framework)` in `full_pipeline.py`.
   - Run the file:
     ```bash
     python full_pipeline.py
     ```

   - The evaluated statements will be saved as `{strategy}_evaluated_statements.xlsx`.

## Calculating F1 MACRO Score

The F1 MACRO score is calculated per model to assess performance.

1. **Set the Model and Prompt Framework**  
   - Navigate to `f1.py` in the `testing` folder.
   - Specify the model and prompt framework(s) for which you want to calculate the F1 score.

2. **Run the Calculation**  
   - Call the `calculate_F1(strategies, model)` function and execute:
     ```bash
     python f1.py
     ```

## Quality Assessment

1. **Set the Model and Prompt Framework**  
   - Go to `quality_assessment.py` in the `testing` folder.
   - Specify the model and prompt framework for quality evaluation.

2. **Run the Quality Assessment**  
   - Call `evaluate_quality(strategy, model)` and execute:
     ```bash
     python quality_assessment.py
     ```
