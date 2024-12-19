# PAPILLON UI



## Key Features ✨

- Privacy-focused prompt generation
- Interactive prompt refinement interface
- Comprehensive edit history tracking

## Prerequisites

- Python 3.7+
- FastAPI
- DSPy
- Language model access (local or cloud-based)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Columbia-NLP-Lab/PAPILLON.git
```

2. Install dependencies:
```bash
pip install fastapi uvicorn jinja2 pydantic dspy
```

3. Configure PAPILLON framework:


## Configuration and Deployment

```bash
cd papillon_ui

python -m sglang.launch_server --model-path <MODEL_IDENTIFIER> --port <PORT> # First launch your local trusted LM server

python app.py --port <PORT> --openai_model <OPENAI_MODEL> --server_port <SERVER_PORT>
```

### Configuration Parameters

The application accepts the following parameters:
- `--port`: Local model host port (default: 3012)
- `--openai_model`: OpenAI model specification (default: gpt-4o-mini)
- `--prompt_file`: DSPy-optimized prompt file path (default: ORIGINAL)
    - If set to "ORIGINAL", the prompt file will be the optimized prompts from the original PAPILLON results stored under `papillon/optimized_prompts`
    - If you have optimized PAPILLON according to your own preferences, you can substitute the path here
- `--model_name`: Huggingface model identifier (default: meta-llama/Llama-3.1-8B-Instruct)
- `--server_port`: FastAPI server port (default: 8012)

### Accessing the Interface

The application interface is available at:
```
http://127.0.0.1:<SERVER_PORT>
```

## Usage Guidelines

1. Input your query through the interface
2. Review the generated privacy-conscious prompt
3. Refine the prompt using the editing interface
4. Submit for processing
5. Review output and modification history

## API Documentation

### Endpoints
- `GET /`: Primary interface
- `POST /generate_prompt`: Initial prompt generation, corresponding to the Prompt Creator step in PAPILLON
- `POST /process_prompt`: Refined prompt processing, corresponding to the Info Aggregator step in PAPILLON



## Support

For technical assistance or feature requests, please:
1. Review existing documentation
2. Check open/closed issues
3. Submit bug reports 

