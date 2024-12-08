# PAPILLON

**First, a motivating example:**

Suppose your original query for ChatGPT is "Generate a cover letter for a research internship position at *[insert research institution here]*, my name is *Siyan Li*, here is my CV: *[insert well-formatted CV texts here]*."; the italicized parts represent Personally Identifiable Information (PII). We have limited control over how our data is used once the servers hosting ChatGPT gains access to it. Therefore, a good way to be privacy-conscious is to prevent your PII to be exposed to ChatGPT in the first place.

Ideally, we want a system we use to prompt a cloud-based LLM such that:
- You receive high-quality responses from the system, which interacts with this cloud-based LLM
- As little of your PII is leaked to this cloud-based LLM as possible

So, we built PAPILLON.

**What is PAPILLON?** 

PAPILLON is a semi-local framework where **trusted but weaker** models (e.g. locally-hosted Llama-3 models) can use **untrusted but more powerful** models as **tools** in order to preserve user inference-time privacy.

<img src="https://drive.google.com/uc?export=view&id=1_65eiWab8cDs3XqP-gNY6i-CDvvEmI56" alt="Overview of the PAPILLON pipeline" height="250"/>


## Getting Started

### To Use PAPILLON on Your Own Data
We have an **end-to-end** tutorial notebook for defining and optimizing your own PAPILLON module using our newest version of PUPA dataset. Please click on the Colab badge below, or refer to the `papillon_tutorial.ipynb` file.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/siyan-sylvia-li/PAPILLON/blob/main/papillon_tutorial.ipynb)

### To Reproduce Our Results
Please refer to the `papillon_v1.0` branch for the original version of our code and data to reproduce the results.

## Installation
We are working on making PAPILLON a PyPI package. Until then, you would unfortunately need to clone the repository first.

To create a conda environment to run PAPILLON in, run the following command:

```
conda create -f environment.yml
conda activate papillon
```

Provide your OpenAI API Key:

```
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

```
python -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --port <PORT_NUMBER>
```

### Running PAPILLON Interactively

This script should display a terminal prompt that allows you to type in your user queries manually, and then print out the corresponding PAPILLON-synthesized privacy-preserving prompt and final PAPILLON responses.

```
cd papillon

python3 run_papillon_interactive.py --port <PORT_NUMBER> --model_name <MODEL_NAME>
```


### Pipeline Optimization
You may use PUPA data or your new data, formatted according to the PUPA format (see `pupa`), to optimize PAPILLON pipelines with different local and API-based model ensembles.

```
cd papillon

python3 run_dspy_optimization_llama.py --port <PORT_NUMBER> --prompt_output "output.json" --data_file "../pupa/PUPA_New.csv"
```

### Evaluating Optimized Pipelines

This will print out the average quality and leakage scores according to the LLM judge defined in `papillon/llm_judge.py`.

```
cd papillon

python3 evaluate_papillon.py --port <PORT_NUMBER> --model_name <MODEL_NAME> (e.g. meta-llama/Llama-3.1-8B-Instruct)
```


## PUPA Dataset
Please see the `pupa` directory for raw CSV files for **PUPA-TNB** and **PUPA-New** datasets. We are currently working on moving the datasets to Huggingface for easier access.

## Adding New Data
If you have new user-assistant interaction data containing private information and you want to process it to the PUPA data format, you can use code in the `pupa` directory to scaffold this process.

## TO-DOs

- [x] Add version of DSPy from the original code base for optimization and inference for reproducibility; currently, PAPILLON is compatible with the newest version of DSPy for inference (interactive mode).
- [x] Complete PUPA data processing code.
- [x] Add PUPA to Huggingface.
- [ ] Build a Flask server and simple UI for PAPILLON.
- [ ] Make PAPILLON installable via PyPI.

## Citation
Here is [the original paper](https://arxiv.org/abs/2410.17127).

If you use PAPILLON in your work, please consider citing it:
```
@article{siyan2024papillon,
  title={PAPILLON: PrivAcy Preservation from Internet-based and Local Language MOdel ENsembles},
  author={Siyan, Li and Raghuram, Vethavikashini Chithrra and Khattab, Omar and Hirschberg, Julia and Yu, Zhou},
  journal={arXiv preprint arXiv:2410.17127},
  year={2024}
}
```
