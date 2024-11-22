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
    modelExampleResponses = dspy.InputField(desc="You have the following information from a better language model responding to related query or queries. Complete the user query by referencing this information. Only you have access to this information.", format=lambda s: f'======\n\n{s.strip()}\n\n======')
    finalOutput = dspy.OutputField()



class PrivacyOnePrompter(dspy.Module):
    def __init__(self, trusted_model, untrusted_model):
        super().__init__()
        self.prompt_creater = dspy.ChainOfThought(CreateOnePrompt)
        self.info_aggregator = dspy.Predict(InfoAggregator)
        self.trusted_model = trusted_model
        dspy.configure(lm=self.trusted_model)
        self.untrusted_model = untrusted_model
        
    
    def forward(self, user_query):
        try:
            prompt = self.prompt_creater(userQuery=user_query)
        except ValueError:
            return dspy.Prediction(
                prompt="",
                output="",
                gptResponse=""
            )
        try:
            response = self.untrusted_model(prompt.createdPrompt)[0]
        except ValueError:
            return dspy.Prediction(
                prompt="",
                output="",
                gptResponse=""
            )
        try:
            final_output = self.info_aggregator(userQuery=user_query, modelExampleResponses=response)
        except ValueError:
            return dspy.Prediction(
                prompt="",
                output="",
                gptResponse=response
            )
        return dspy.Prediction(
            prompt=prompt.createdPrompt,
            output=final_output.finalOutput,
            gptResponse=response
        )
