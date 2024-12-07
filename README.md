# PAPILLON v1.0

This branch contains code and data needed to replicate our original paper, [PAPILLON: PrivAcy Preservation from Internet-based and Local Language MOdel ENsembles](https://arxiv.org/abs/2410.17127). We have done some cleanup of the code base but the semantics are left unchanged.

## Installation

To create a conda environment to run PAPILLON in, run the following command:

```bash
conda create -n papillon python=3.10
pip install openai pandas sglang[all]
# Install a specific commit of DSPy
pip install git+https://github.com/stanfordnlp/dspy.git@commit ee8206ea7ce14630b3e64d2b997878169dee3252
```

Provide your OpenAI API Key:

```bash
export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

## Using PAPILLON

To use the DSPy-optimized PAPILLON pipeline, you would need to do the following:

1. Host your trusted model of choice on a server
2. Supply private user prompts 
3. Run the provided PAPILLON pipeline or optimize new PAPILLON pipelines on new data

We will build a Flask server and UI for PAPILLON for easy use in the future. For now, you would have to manually enter the private user query, or read queries from a CSV file.

You can interact with PAPILLON pipelines directly using the `papillon/run_papillon_interactive.py` script.

### Host Language Models on Server
We currently have optimized PAPILLON prompts for the following models:

- Llama-3.2-1B-Instruct
- Llama-3.2-3B-Instruct
- Llama-3-8B-Instruct
- Llama-3.1-8B-Instruct
- Mistral-7B-Instruct
- Mistral-Small

There are multiple options to host these models. For Llama-3.2, the current official method of hosting is via [VLLM](https://docs.vllm.ai/en/latest/). You can also host the 1B and 3B models on [Ollama](https://ollama.com/library/llama3.2). The other models can be hosted through [SGLang](https://sgl-project.github.io/). Here, we use SGLang as an example:

```bash
python -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --port <PORT_NUMBER>
```

### Pipeline Optimization
Use the original version of PUPA to optimize PAPILLON pipelines with different local and API-based model ensembles.

```bash
cd papillon

python3 run_dspy_optimization_llama.py --port <PORT_NUMBER> --prompt_output "output.json" --data_file "../pupa/PUPA_New.csv"
```

### Evaluating Optimized Pipelines

This will print out the average quality and leakage scores according to the LLM judge defined in `papillon/llm_judge.py`.

```bash
cd papillon

python3 evaluate_papillon.py --port <PORT_NUMBER> --model_name <MODEL_NAME> (e.g. meta-llama/Llama-3.1-8B-Instruct)
```

## PUPA Dataset
Please see the `pupa` directory for raw CSV files for **PUPA-TNB** and **PUPA-New** datasets. These are the original versions of the dataset, so they are not the most up-to-date. To find the most up-to-date version of PUPA, please refer to the main branch and the corresponding Huggingface repository.
