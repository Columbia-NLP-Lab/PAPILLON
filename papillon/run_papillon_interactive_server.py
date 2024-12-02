from run_llama_dspy import PrivacyOnePrompter
from argparse import ArgumentParser
import dspy
from evaluate_papillon import parse_model_prompt

from flask import Flask, render_template, request
from flask_session import Session
from flask_cors import CORS
import logging
import json

# Create the Flask app instance
app = Flask(__name__)

LOGGER = logging.getLogger('gunicorn.error')

SECRET_KEY = 'YOURKEY'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

Session(app)
CORS(app)


# Define a route for the root URL
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

# First get the synthesized prompt
@app.route("/synth_prompt", methods=["POST"])
def get_synthesized_prompt():
    data = request.form.get('json')
    if data:
        data = json.loads(data)
    else:
        data = {}
    print(data)
    if "user_query" in data:
        user_query = data["user_query"]
        prompt = priv_prompt.prompt_creater(userQuery=user_query)
        return {
            "prompt": prompt.createdPrompt
        }
    return {
        "prompt": ""
    }

# Get the GPT response
@app.route("/untrusted_response", methods=["POST"])
def get_untrusted_response():
    data = request.form.get("json")
    if data:
        data = json.loads(data)
    else:
        data = {}
    if "papillon_prompt" in data:
        papillon_prompt = data["papillon_prompt"]
        response = openai_lm(papillon_prompt)[0]
        return {
            "untrusted_response": response
        }
    return {
        "untrusted_response": ""
    }

# Get the final output
@app.route("/final_response", methods=["POST"])
def get_final_response():
    data = request.form.get("json")
    if data:
        data = json.loads(data)
    else:
        data = {}
    if "untrusted_response" in data:
        final_output = priv_prompt.info_aggregator(userQuery=data["user_query"], modelExampleResponses=data["untrusted_response"])
        return {
            "final_response": final_output.finalOutput
        }
    return {
        "final_response": ""
    }


# Run the app if this script is executed directly
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, help="The port where you are hosting your local model")
    parser.add_argument("--openai_model", type=str, default="gpt-4o-mini")
    parser.add_argument("--prompt_file", type=str, default="ORIGINAL", help="The DSPy-optimized prompt, stored as a json file")
    parser.add_argument("--model_name", type=str, help="The Huggingface identifier / name for your local LM")
    parser.add_argument("--server_port", type=int, help="Where you are hosting your SERVER, not models")
    
    args = parser.parse_args()

    if args.prompt_file == "ORIGINAL":
        args.prompt_file = parse_model_prompt(args.model_name)
    
    local_lm = dspy.LM(f'openai/{args.model_name}', api_base=f"http://0.0.0.0:{args.port}/v1", api_key="", max_tokens=4000)
    dspy.configure(lm=local_lm)

    openai_lm = dspy.OpenAI(model=args.openai_model, max_tokens=4000)

    priv_prompt = PrivacyOnePrompter(local_lm, openai_lm)
    
    priv_prompt.load(args.prompt_file, use_legacy_loading=True)

    app.run(debug=True, port=args.server_port)

