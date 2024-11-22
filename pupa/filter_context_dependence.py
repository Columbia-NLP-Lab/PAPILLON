import pandas

import openai

client = openai.OpenAI(api_key="<YOUR_OPENAI_API_KEY>")


def context_independence(query, history):
    msgs = [{"role": "system", "content": f"Given a user query and a conversation history, does the completion of the query depend on the conversation history? Respond with yes or no.\n\nUSER QUERY: {query}\n\nCONVERSATION HISTORY: {history}"}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=msgs
    )
    return response.choices[0].message.content.lower().startswith("no")
