import pandas
from run_dspy_optimization_llama import metric_finegrained
from dspy import Example
import dspy
import tqdm
import litellm
from argparse import ArgumentParser
from run_llama_dspy import PAPILLON

def parse_model_prompt(model_name):
    model_name = model_name.lower()
    if "llama" in model_name:
        if "1b-instruct" in model_name:
            return "optimized_prompts/llama_32_1b_instruct_prompt.json"
        elif "3b-instruct" in model_name:
            return "optimized_prompts/llama_32_3b_instruct_prompt.json"
        elif "8b-instruct" in model_name:
            if "3.1" in model_name:
                return "optimized_prompts/llama_31_8b_instruct_prompt.json"
            else:
                return "optimized_prompts/llama_3_8b_instruct_prompt.json"
    elif "mistral" in model_name:
        if "small" in model_name:
            return "optimized_prompts/mistral_small_prompt.json"
        elif "7b" in model_name:
            return "optimized_prompts/mistral_7b_instruct_prompt.json"
    raise NotImplementedError("Model currently not supported! You will have to optimize it yourself!")

    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, help="The port where you are hosting your local model")
    parser.add_argument("--data_file", type=str, help="The data file containing PUPA-style queries and target responses")
    parser.add_argument("--openai_model", type=str, default="gpt-4o-mini")
    parser.add_argument("--prompt_file", type=str, default="ORIGINAL", help="The DSPy-optimized prompt, stored as a json file")
    parser.add_argument("--model_name", type=str, help="The Huggingface identifier / name for your local LM")
    parser.add_argument("--output_file_name", type=str, default="output.csv")
    args = parser.parse_args()
    
    data_file = pandas.read_csv(args.data_file)
    qual_scores = []
    leak_scores = []
    all_user_queries = []
    target = []
    new_completion = []
    new_prompt = []
    all_pii = []

    local_lm = dspy.LM(f'openai/{args.model_name}', api_base=f"http://0.0.0.0:{args.port}/v1", api_key="", max_tokens=4000)
    dspy.configure(lm=local_lm)

    openai_lm = dspy.OpenAI(model=args.openai_model, max_tokens=4000)
    
    priv_prompt = PAPILLON(openai_lm)
    

    if args.prompt_file == "ORIGINAL":
        args.prompt_file = parse_model_prompt(args.model_name)
    
    priv_prompt.load(args.prompt_file, use_legacy_loading=True)

    
    for i, row in tqdm.tqdm(data_file.iterrows()):
        gold = Example({"target_response": row["target_response"],
                        "user_query": row["user_query"],
                        "pii_str": row["pii_units"]}).with_inputs("user_query")
        try:
            pred = priv_prompt(row["user_query"])
        except litellm.exceptions.BadRequestError:
            continue
        if row["target_response"] is not None and isinstance(row["target_response"], str) and isinstance(row["pii_units"], str):
            qual, leak = metric_finegrained(gold, pred, openai_lm)
            print(qual, leak)
            
            if qual != -1 and leak != -1:
                qual_scores.append(qual)
                all_user_queries.append(row["user_query"])
                leak_scores.append(leak)
                target.append(row["target_response"])
                new_completion.append(pred.output)
                new_prompt.append(pred.prompt)
                all_pii.append(row["pii_units"])
            result_df = pandas.DataFrame()
            result_df["quals"] = qual_scores
            result_df["leaks"] = leak_scores
            result_df["queries"] = all_user_queries
            result_df["targets"] = target
            result_df["papillon_completion"] = new_completion
            result_df["papillon_prompt"] = new_prompt
            result_df["pii_str"] = all_pii 
            result_df.to_csv(args.output_file_name)
    
    print("AVERAGE QUALITY SCORE", sum(qual_scores) / len(qual_scores))
    print("AVERAGE LEAKAGE SCORE", sum(leak_scores) / len(leak_scores))
    print("==============")
    