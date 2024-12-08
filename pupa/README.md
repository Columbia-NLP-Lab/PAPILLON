# Overview
This repository details the code you can use to convert any single-turn user-assistant interactions into PUPA-style data. This directory also contains the raw csv files for the PUPA dataset.

# PUPA Data Format
To make your data compatible with the code in the `papillon` directory, your data file should have the following columns:
- `user_query`: The original user query with private information
- `target_response`: This is only relevant if you want to evaluate different PAPILLON pipelines. The `target_response` column records the "ideal" response the pipeline should produce given the user query. You can generate this by directly passing the user query to an API-based LLM.
- `pii_units`: The list of PII units joined by "||".
- `redacted_query`: LLM-generated redaction of the original user query to remove private information.

# Formatting New Data

Assuming you have a series of user-assistant dialogues, where the user reveals private information.

For each turn of the dialogue, you would run the `process_query_response_pairs` function in `turn_processor.py`. You would need to pass in:

1. The current user query
2. The ideal assistant response
3. The conversational history; we need this to determine whether a user-assistant turn is contextually independent. We only include the contextually-independent turns since PAPILLON currently does not support multi-turn interactions. 