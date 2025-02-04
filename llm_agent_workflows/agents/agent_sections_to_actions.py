import json

from typing import List, Dict, Union

from crew import Agent, Task


class AgentSectionsToActions(Agent):

    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        # Set required attributes
        self.role = "KYC Compliance Officer"
        self.goal = "Identify KYC-relevant sections from a given policy, map each action to the required data points, Format the output into a structured JSON format."
        self.backstory = "With over 10 years of experience in financial compliance, the KYC Compliance Officer has worked with global financial institutions, helping them align with international AML/KYC regulations like FATF, FINCEN, and GDPR. They use a structured approach to ensure data accuracy and compliance integrity."

        self.bedrock_client = bedrock_client or self._init_bedrock_client()


    def _analyze_page(self, page_content: Dict[str, Union[str, List[str]]], page_num: int) -> Dict[str, str]:
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

    def task_section_to_actions(self) -> Task:
        """Task: Convert document sections into actionable items."""
        section = " Where a firm advises the owners of securities, in respect of the repurchase, exchange or redemption by an issuer of those securities, the owners will be customers of the firm for AML purposes."
        # things to do
        # 1. separate the policy section into individual
        # 2. make sure the policy has actionable items
        # 3. add data points to the actionable items

        return Task(
            description=f"The primary objective of this task is to process a given KYC policy document section. ({section}) and extract KYC-related actions while identifying the corresponding data points associated with each action. This ensures compliance with regulatory frameworks such as FATF, FINCEN, GDPR, and AML directives. The process follows, to identifying key KYC actions such as verification, monitoring, reporting, and record-keeping, and map the extracted actions to specific data points (e.g., Name, ID, Source of Funds).",
            agent_role="KYC Compliance Officer",
            expected_output="Matrix format showing the section, action, and data point.",
            dependencies=[]
        )