import json

from typing import List, Dict, Union

from crew import Agent

class AgentEvidenceProcess(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def _evidence_clean(self, evidence: str) -> str:
        """Process extracted text evidence."""

        prompt = f"""
        You are a highly intelligent assistant designed to clean and format extracted text. The text comes from OCR (Optical Character Recognition) results and may contain raw, unformatted information. Your job is to:

        1. Clean the text by removing any unnecessary characters, extra spaces, line breaks, or other noise.
        2. Identify key information for KYC such as dates, phone numbers, email addresses, possibly names or addresses, etc.
        3. Format the extracted information in a structured and readable way. Ensure each type of information is properly labeled.

        **Instructions:**
        - If a date is identified (e.g., in formats such as `MM/DD/YYYY` or `DD/MM/YYYY`), format it as: `Date: [formatted date]`.
        - If a phone number is identified (e.g., in formats such as `+1 (555) 123-4567`), format it as: `Phone: [formatted phone number]`.
        - If an email address is identified (e.g., in formats such as `example@email.com`), format it as: `Email: [formatted email]`.
        - Remove any irrelevant information such as extra punctuation or broken text.

        Here is the text extracted from the image using OCR:
            {evidence}
        """

        response = self.invoke_bedrock(prompt)

        return response

    #TODO: change type of user inside the prompt and method vars, depending on how we pull the data
    def _risk_assessment(self, risks: List[str], complete_profile: List[str]) -> str:
        """Process extracted text evidence."""

        prompt = f"""
        You are an KYC expert designed to assess risk based on a set of questions and user profile information. The questions will be provided as a list, and the answers to these questions will be inferred based on the user's profile information, which will be provided as text. After evaluating the responses, assign a risk tier and provide a risk summary in a structured JSON format.
        
        **Instructions:**
        1. **Input Variables:**
           - **Questions (List)**: A list of questions that need to be answered based on the user profile information. Each question is to be answered according to the user profile text.
           - **User Profile (Text)**: A detailed description of the user's profile, including their age, occupation, health status, location, or other relevant information.
        
        2. **Task**:
           - For each question in the list, infer an answer based on the provided user profile.
           - Based on the inferred answers, assign a **risk tier**: 
             - **Low Risk**: The user shows minimal or no significant risk.
             - **Medium Risk**: The user has some moderate risk factors.
             - **High Risk**: The user has significant risk factors requiring attention.
           - Provide a **risk summary** that explains how the answers to the questions and the user profile contributed to the risk tier assessment.
        
        3. **Output Format**:
           - The output should be a JSON object with the following keys:
             - **risk_tier**: The risk tier assigned to the user (Low, Medium, High).
             - **risk_summary**: A brief summary of the risk evaluation based on the user's profile and answers.
        
        **Input Example**:
        - **Questions (List)**:
            {risks}
        - **User Profile (text)**:
            {complete_profile}
        """

        response = self.invoke_bedrock(prompt)

        return response

