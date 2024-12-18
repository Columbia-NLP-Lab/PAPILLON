# PAPILLON UI



## Key Features ✨

- Privacy-focused prompt generation
- Interactive prompt refinement interface
- Comprehensive edit history tracking
- Seamless integration with local and cloud LLMs
- Privacy-oriented optimization pipeline

## Prerequisites

- Python 3.7+
- FastAPI
- DSPy framework
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

3. Configure Papillon framework:


## Configuration and Deployment

### Standard Deployment
```bash
python app.py
```

### Advanced Configuration
```bash
python app.py --port 3012 --openai_model gpt-4-mini --server_port 8012
```

### Configuration Parameters

The application accepts the following parameters:
- `--port`: Local model host port (default: 3012)
- `--openai_model`: OpenAI model specification (default: gpt-4o-mini)
- `--prompt_file`: DSPy-optimized prompt file path
- `--model_name`: Huggingface model identifier (default: meta-llama/Llama-3.1-8B-Instruct)
- `--server_port`: FastAPI server port (default: 8012)

### Accessing the Interface

The application interface is available at:
```
http://127.0.0.1:8012
```

## Usage Guidelines

1. Input your query through the interface
2. Review the generated privacy-conscious prompt
3. Refine the prompt using the editing interface
4. Submit for processing
5. Review output and modification history

## System Architecture

The application implements a sophisticated pipeline:
1. Initial prompt generation
2. User-driven refinement
3. Language model processing
4. Privacy-aware output synthesis

## Privacy Framework

The system prioritizes privacy through:
- Pre-processing prompt review
- Comprehensive change tracking
- Local model processing options
- Privacy-focused output verification

## API Documentation

### Endpoints
- `GET /`: Primary interface
- `POST /generate_prompt`: Initial prompt generation
- `POST /process_prompt`: Refined prompt processing



## Support

For technical assistance or feature requests, please:
1. Review existing documentation
2. Check open/closed issues
3. Submit bug reports 

