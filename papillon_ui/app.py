# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import sys
sys.path.insert(1, "../papillon")
from run_llama_dspy import PrivacyOnePrompter
from argparse import ArgumentParser
import dspy
from evaluate_papillon import parse_model_prompt
import json

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Query(BaseModel):
    query: str

class PromptEdit(BaseModel):
    original_prompt: str
    edited_prompt: str

class FinalInput(BaseModel):
    original_query: str
    original_prompt: str
    edited_prompt: str
    

class Pipeline:
    def __init__(self):
        self.edit_history = []
    
    def generate_initial_prompt(self, user_query: str) -> str:
        initial_prompt = priv_prompt.prompt_creater(userQuery=user_query)
        return initial_prompt.createdPrompt
    
    def record_edit(self, original_prompt: str, edited_prompt: str, timestamp: str) -> dict:
        """Record the edits made by the user"""
        edit = {
            'timestamp': timestamp,
            'original': original_prompt,
            'edited': edited_prompt,
            'diff_length': len(edited_prompt) - len(original_prompt)
        }
        self.edit_history.append(edit)
        return edit
    
    def call_cloud_llm(self, prompt: str) -> str:
        """
        Placeholder for cloud LLM API call
        Replace with actual API implementation
        """
        return openai_lm(prompt)[0]
    
    def synthesize_output(self, llm_response: str, user_query: str) -> str:
        """
        Placeholder for output synthesis
        Add your post-processing logic here
        """
        return priv_prompt.info_aggregator(userQuery=user_query, modelExampleResponses=llm_response).finalOutput

pipeline = Pipeline()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_prompt")
async def generate_prompt(query: Query):
    initial_prompt = pipeline.generate_initial_prompt(query.query)
    return JSONResponse(content={'prompt': initial_prompt})

@app.post("/process_prompt")
async def process_prompt(final_input: FinalInput):
    # Record the edit
    edit_record = pipeline.record_edit(
        final_input.original_prompt,
        final_input.edited_prompt,
        datetime.now().isoformat()
    )
    
    # Process through pipeline
    llm_response = pipeline.call_cloud_llm(final_input.edited_prompt)
    final_output = pipeline.synthesize_output(llm_response, final_input.original_query)
    
    return JSONResponse(content={
        'output': final_output,
        'edit_record': edit_record
    })

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, help="The port where you are hosting your local model", default=3012)
    parser.add_argument("--openai_model", type=str, default="gpt-4o-mini")
    parser.add_argument("--prompt_file", type=str, default="ORIGINAL", help="The DSPy-optimized prompt, stored as a json file")
    parser.add_argument("--model_name", type=str, help="The Huggingface identifier / name for your local LM", default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--server_port", type=int, help="Where you are hosting your SERVER, not models", default=8012)
    
    args = parser.parse_args()

    if args.prompt_file == "ORIGINAL":
        args.prompt_file = parse_model_prompt(args.model_name)
    
    local_lm = dspy.LM(f'openai/{args.model_name}', api_base=f"http://0.0.0.0:{args.port}/v1", api_key="", max_tokens=4000)
    dspy.configure(lm=local_lm)

    openai_lm = dspy.OpenAI(model=args.openai_model, max_tokens=4000)

    priv_prompt = PrivacyOnePrompter(local_lm, openai_lm)
    
    priv_prompt.load("../papillon/" + args.prompt_file, use_legacy_loading=True)


    print("Starting FastAPI server...")
    print(f"You can access it at: http://127.0.0.1:{args.server_port}")
    uvicorn.run(app, host="0.0.0.0", port=args.server_port)


