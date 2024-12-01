from create_privacy_span import process_user_query
from filter_context_dependence import context_independence

def process_query_response_pairs(query, response, history):
    if not context_independence(query, history):
        return None
    pii_units, redacted_query = process_user_query(query)
    return {
        "user_query": query,
        "target_response": response,
        "pii_units": pii_units,
        "redacted_query": redacted_query
    }

if __name__ == "__main__":
    query = "<ORIGINAL_USER_QUERY>"
    response = "<ORIGINAL_CHATBOT_RESPONSE>"
    history = "<ORIGINAL_CONVERSATION_HISTORY>"
    print(process_query_response_pairs(query, response, history))