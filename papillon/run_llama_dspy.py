import dspy


import os; os.environ['LITELLM_LOG'] = 'ERROR'


class CreateOnePrompt(dspy.Signature):
    """
    You are a helpful assistant that is very mindful of user privacy. You have access to a powerful large language model that you can query. Given a user request, create a prompt for your large language model that preserves user privacy, so that this model can help you complete the user request. Provide the prompt directly without any preamble. DO NOT COMPLETE THE USER QUERY, ONLY GENERATE A PROMPT.
    """
    userQuery = dspy.InputField(desc="The user's request to be fulfilled.")
    createdPrompt = dspy.OutputField()

class InfoAggregator(dspy.Signature):
    """
    You are a helpful assistant. Respond to queries from the user.
    """

    userQuery = dspy.InputField(desc="The user's request to be fulfilled.")
    modelExampleResponses = dspy.InputField(desc="Information from a more powerful language model responding to related queries. Complete the user query by referencing this information. Only you have access to this information.")
    finalOutput = dspy.OutputField()


class PAPILLON(dspy.Module):
    def __init__(self, untrusted_model):
        self.prompt_creater = dspy.ChainOfThought(CreateOnePrompt)
        self.info_aggregator = dspy.Predict(InfoAggregator)
        self.untrusted_model = untrusted_model

    def forward(self, user_query):
        try:
            prompt = self.prompt_creater(userQuery=user_query).createdPrompt
            response = self.untrusted_model(prompt)[0]
            output = self.info_aggregator(userQuery=user_query, modelExampleResponses=response)
        except Exception:
            return dspy.Prediction(prompt="", output="", gptResponse="")

        return dspy.Prediction(prompt=prompt, output=output.finalOutput, gptResponse=response)