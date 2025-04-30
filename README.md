# Comparing Evidence Retrieval Strategies in AFC

This repository provides code to compare and evaluate different evidence retrieval strategies in Automated Fact-Checking. The project is organized by three primary components:

1. **Models** 
2. **Retrievers** 
3. **Prompt Frameworks**

As of now, there are two models (GPT-4 and Llama 3.1), one main retriever (Serper websearch), and four prompt frameworks that each represent a particular retrieval strategy as well as a baseline.

The strategies are:

- **Basic retrieval**: Keyword search  
- **Question-Guided Retrieval**: RARR  
- **Multihop Retrieval**: HiSS  
- **Iterative Refinement**: CoRAG  

(The baseline approach is also included for comparison.)

---

## Setup

1. **Install Dependencies**  
   Make sure you have Python 3.9+ installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install the Project in Editable Mode**  
   From the project root directory, install in “editable” mode:
   ```bash
   pip install -e .
   ```

3. **Configure API Keys**  
   Obtain the following API keys and store them in a `.env` file in the root directory:
   - `OPENAI_API_KEY`
   - `SERP_API_KEY`

   Your `.env` should look like:
   ```
   OPENAI_API_KEY=YOUR_OPENAI_KEY
   SERP_API_KEY=YOUR_SERP_KEY
   ```

---

## Running Tests and Evaluations

1. **Navigate to the testing folder**  
   ```bash
   cd testing
   ```

2. **Run the Retrieval Pipeline**  
   To evaluate the dataset using a specific **model** and one or more **strategies**, run:
   ```bash
   python full_pipeline.py --model {model} --strategy {strategy1} {strategy2} ...
   ```
   - Valid model choices: `gpt4`, `llama8b`  
   - Valid strategy choices: `baseline`, `keyword`, `rarr`, `hiss`, `ragar`  

   For example:
   ```bash
   python full_pipeline.py --model gpt4 --strategy baseline keyword
   ```

   The results will be saved as `{strategy}_{model}_AVERITEC.xlsx`. Each file contains:  
   - The statement being evaluated  
   - Original veracity  
   - Predicted veracity  
   - Explanation  
   - Retrieved information  
   - Gold evidence  

3. **Evaluate Overall Performance**  
   To calculate accuracy and AveriTeC scores for one or more strategies, run:
   ```bash
   python scores.py --model {model} --strategy {strategy1} {strategy2} ...
   ```
   For example:
   ```bash
   python scores.py --model gpt4 --strategy baseline rarr hiss
   ```
   The results will be saved as `results_averitec_snippet/{model}/scores_{model}.xlsx`, showing metrics for each strategy requested.

---

## License

[MIT License](LICENSE)

Feel free to modify or extend the code to incorporate additional models, retrievers, or custom prompt frameworks.