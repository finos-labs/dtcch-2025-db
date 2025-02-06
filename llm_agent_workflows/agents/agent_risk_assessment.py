from typing import List
from crew import Agent


class AgentRiskAssessment(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    # TODO: change type of user inside the prompt and method vars, depending on how we pull the data
    def _risk_assessment(self, risks: str, complete_profile: str) -> str:
        """Process extracted text evidence."""

        prompt = f"""
        You are an KYC expert designed to assess risk based on a set of questions and user profile information. The questions will be provided as a list, and the answers to these questions will be inferred based on the user's profile information, which will be provided as text. After evaluating the responses, assign a risk tier and provide a risk summary in a structured JSON format.

        Instructions:
        1. Input Variables:
           - Questions: A list of questions that need to be answered based on the user profile information. Each question is to be answered according to the user profile text.
           - User Profile: A detailed description of the user's profile, including their age, occupation, health status, location, or other relevant information.

        2. Task
           - For each question in the list, infer an answer based on the provided user profile.
           - Then use this inferred answers, assign a risk tier: 
             - Low : The user shows minimal or no significant risk.
             - Medium: The user has some moderate risk factors.
             - High: The user has significant risk factors requiring attention.
           - Then use this inferred answers, provide a risk summary that explains how the answers to the questions and the user profile contributed to the risk tier assessment.

        Provide your response without verbosity and return format your response as JSON with the following structure:
        {{
            "risk_tier": "The risk tier assigned to the user (Low, Medium, High).",
            "risk_summary": "A complete summary of the risk evaluation and factor based on the inferred answeres."
        }}
        Input:
        - Questions:
            {risks}
        - User Profile:
            {complete_profile}
        """

        response = self.invoke_bedrock(prompt)

        return response

