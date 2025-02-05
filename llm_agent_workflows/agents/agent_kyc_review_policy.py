from crew import Agent, Task


class AgentKYCReviewPolicy(Agent):

    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        # Set required attributes for agent
        self.role = "kyc_analyst"
        self.goal = ""  # Independent for every task
        self.backstory = "With over 10 years of experience in financial compliance, the KYC Compliance Officer has worked with global financial institutions, helping them align with international AML/KYC regulations like FATF, FINCEN, and GDPR. They use a structured approach to ensure data accuracy and compliance integrity."
        self.bedrock_client = bedrock_client or self._init_bedrock_client()


    def task_document_to_section(self, page_num) -> Task:
        """Task: Convert document sections into actionable items, separate document section to policy and check if is actionable."""
        self.goal = "Identify KYC-relevant sections from a given policy, map each action to the required data points, Format the output into a structured JSON format."
        return Task(
            description=f"""Analyze the following page {page_num} content and provide:
                1. Up to 5 relevant labels that categorize the main topics or themes
                2. A comprehensive summary that captures all important information
                
                Content: {page_content['text']}
                
                Additional Context: This page contains {len(page_content['images'])} images.
                
                Please format your response as JSON with the following structure:
                {{
                    "labels": ["label1", "label2", ...],
                    "summary": "detailed summary"
                }}
                """,
            agent_role="kyc_analyst",
            expected_output="Matrix format showing the section, action, and data point.",
            dependencies=[],
            validation_type="json"
        )
    
    def task_section_to_actions(self, previous_task) -> Task:
        """Task: Convert document sections into actionable items, separate document section to policy and check if is actionable."""
        self.goal = "Identify KYC-relevant sections from a given policy, map each action to the required data points, Format the output into a structured JSON format."
        return Task(
            description=f"The primary objective of this task is to process a given KYC policy document section. ({previous_task.context}) and extract KYC-related actions while identifying the corresponding data points associated with each action. This ensures compliance with regulatory frameworks such as FATF, FINCEN, GDPR, and AML directives. The process follows, to identifying key KYC actions such as verification, monitoring, reporting, and record-keeping, and map the extracted actions to specific data points (e.g., Name, ID, Source of Funds).",
            agent_role="kyc_analyst",
            expected_output="Matrix format showing the section, action, and data point.",
            dependencies=[previous_task],
            validation_type="json"
        )

    def task_actions_to_data_points(self, previous_task) -> Task:
        """Task: Convert document actionable items to data points"""
        self.goal = "Process actions and requirements to actual data points required from the client to complete KYC"

        return Task(
            description=f"""
                You are an expert in KYC (Know Your Customer) compliance and data mapping. 
                Your task is to analyze a given text and determine whether it contains a KYC action. 
                If it does, extract the corresponding data point required for compliance.
                
                Below are the steps you need to follow:
                1. Analyze the input text carefully. The input may or may not contain a KYC-related action. If the text does not contain a clear action, respond with "No Action Detected"
                2. Identify if the text describes an action related to KYC. KYC actions usually involve identifying, verifying, confirming, conducting screening, or assigning roles.
                3. Extract the corresponding KYC data point. The data point is the key piece of information that must be collected to complete the action. Common data points include: "First name", "Last name", "Role", "Residential Address", "Screening Result", "UBO Role", etc
                4. Format your response in the following structure:
                {{
                "quote": <Complete original document line from which you extract the action>
                "action_detected": true,
                "action": "<Extracted KYC Action>",
                "data_point": "<Corresponding Data Point>"
                }}
                If no action is found, return:
                {{
                "action_detected": false
                }}
                5. Please only and only output a single json string with all the results together in one json and nothing else so that it can be parsed.
                
                Please do it for the following item in the list individually: {previous_task.context}
                """,
            agent_role="kyc_analyst",
            expected_output="map a data point from an action relevant for KYC",
            # TODO: add it on a csv file and use the process to read from the file, so in future we can add more
            context=f"""
                Below are some examples where first we have the action and then the data point after the comma for your understanding:
                Create Natural Person Client Senior Manager profile for identified Client Senior Managers, Natural Person Client Senior Manager Role
                Identify the first name of any Natural Person Client Senior Managers (CSMs), First name
                Identify the middle name of any Natural Person Client Senior Managers (CSMs), Middle name
                Verify the middle name of any Natural Person Client Senior Managers (CSMs), Middle name
                Identify the last name of any Natural Person Client Senior Managers (CSMs), Last name
                Verify the last name of any Natural Person Client Senior Managers (CSMs), Last name
                Identify the Natural Person Client Senior Manager's role at the client?, Role
                Conduct screening on the Natural Person Client Senior Manager, Screening Result
                Has a Client Senior Manager been identified as a Relative or Close Associate of a Politically Exposed Person?, RCA Flag
                Confirm if a Client Senior Manager have significant control of the client, Significant control
                Confirm if KYC Ops agree with ACO assessment of Client Senior Manager's Significant control, Significant control KYC Ops agreement
                Add Ultimate Beneficial Owner role to Client Senior Manager with Significant control, UBO role
                """,
            dependencies=[previous_task],
            validation_type="json"
        )