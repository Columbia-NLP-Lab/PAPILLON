import dspy


class JudgeQuality(dspy.Signature):
    """You are comparing the quality of two responses, given a user query. Is response A at least as good as response B? Respond with yes or no."""

    user_query = dspy.InputField(desc="The user's request to be fulfilled.")
    response_A = dspy.InputField()
    response_B = dspy.InputField()
    output = dspy.OutputField()

class JudgeLeakage(dspy.Signature):
    """Determine whether a piece of information is present in the prompt given. Respond with yes or no."""

    information_piece = dspy.InputField(desc="The piece of information that we wish to check. If this piece of information is a celebrity name, respond with no.")
    prompt = dspy.InputField()
    output = dspy.OutputField()

class JudgePromptQual(dspy.Signature):
    """Determine whether a piece of text is a valid prompt for a language model. Respond with yes or no."""
    prompt_input = dspy.InputField()
    output = dspy.OutputField()


class LLMJudge(dspy.Module):
    def __init__(self):
        super().__init__()
        self.quality_judge = dspy.ChainOfThought(JudgeQuality)
        self.fact_checker = dspy.Predict(JudgeLeakage)
        self.prompt_qual = dspy.ChainOfThought(JudgePromptQual)

    def forward(self, user_query, og_resp, new_resp=None, updated_query=None, pii_str=None):
        if new_resp:
            answer = self.quality_judge(user_query=user_query, response_A=new_resp, response_B=og_resp)
            judgment_1 = int((answer.output.lower()).startswith("yes"))
            answer = self.quality_judge(user_query=user_query, response_A=og_resp, response_B=new_resp)
            judgment_2 = int((answer.output.lower()).startswith("yes"))
            judgment = process_scores(judgment_1, judgment_2)
        else:
            judgment = -1
        if updated_query:
            if isinstance(pii_str, str):
                all_pii_pieces = set(pii_str.split("||"))
                pii_score = 0
                for p in all_pii_pieces:
                    answer = self.fact_checker(information_piece=p, prompt=updated_query)
                    pii_score += int((answer.output.lower()).startswith("yes"))
            else:
                pii_score = -1
            ans = self.prompt_qual(prompt_input=updated_query)
            prompt_score = int((ans.output.lower()).startswith("yes"))
        else:
            pii_score = -1
            prompt_score = -1
        
        return dspy.Prediction(
            quality=judgment,
            leakage=pii_score,
            prompt=prompt_score
        )


def process_scores(s1, s2):
    if s1 == s2:
        return 1
    return s1

