import json

from typing import List, Dict, Union

from crew import Agent

class AgentRiskAssessment(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        self.role = ""
        self.goal = ""
        self.backstory = ""
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def risk_asse(self, page_content: Dict[str, Union[str, List[str]]], page_num: int) -> Dict[str, str]:
        """Analyze a page using AWS Bedrock."""
        # Prepare the prompt
        prompt = f"""Analyze the following page {page_num} content and provide:
        1. Up to 5 relevant labels that categorize the main topics or themes
        2. A comprehensive summary that captures all important information
        
        Content: {page_content['text']}
        
        Additional Context: This page contains {len(page_content['images'])} images.
        
        Please format your response as JSON with the following structure:
        {{
            "labels": ["label1", "label2", ...],
            "summary": "detailed summary"
        }}
        """
        
        response = self.invoke_bedrock(prompt)
        try:
            if not response:
                return {"labels": [], "summary": "Error analyzing page"}
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Error parsing response for page {page_num}")
            return {"labels": [], "summary": "Error analyzing page"}
