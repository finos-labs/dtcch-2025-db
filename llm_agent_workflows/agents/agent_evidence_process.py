import json

from typing import List, Dict, Union

from crew import Agent

class AgentEvidenceProcess(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def evidence_process(self, evidence: str) -> str:
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

