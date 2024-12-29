from run_llama_dspy import PAPILLON
from argparse import ArgumentParser
import dspy
from evaluate_papillon import parse_model_prompt

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, help="The port where you are hosting your local model")
    parser.add_argument("--openai_model", type=str, default="gpt-4o-mini")
    parser.add_argument("--prompt_file", type=str, default="ORIGINAL", help="The DSPy-optimized prompt, stored as a json file")
    parser.add_argument("--model_name", type=str, help="The Huggingface identifier / name for your local LM")
    
    args = parser.parse_args()

    if args.prompt_file == "ORIGINAL":
        args.prompt_file = parse_model_prompt(args.model_name)
    
    local_lm = dspy.LM(f'openai/{args.model_name}', api_base=f"http://0.0.0.0:{args.port}/v1", api_key="", max_tokens=4000)
    dspy.configure(lm=local_lm)

    openai_lm = dspy.OpenAI(model=args.openai_model, max_tokens=4000)

    priv_prompt = PAPILLON(openai_lm)
    
    priv_prompt.load(args.prompt_file, use_legacy_loading=True)

    while True:
        user_query = input("Your Query > ")
        pred = priv_prompt(user_query)
        print("PAPILLON PROMPT > ", pred.prompt)
        print("PAPILLON OUTPUT > ", pred.output)

