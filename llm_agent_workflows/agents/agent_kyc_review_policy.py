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

    def task_section_to_actions(self, section) -> Task:
        """Task: Convert document sections into actionable items, separate document section to policy and check if is actionable."""
        self.goal = "Convert section to individual sentences"
        return Task(
            description=f"The primary objective of this task is to process a given KYC policy document section, separate them by sentences. ({section}).",
            agent_role="kyc_analyst",
            expected_output="Json with the separated sentences",
            dependencies=[],
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
                4. Please format your response as JSON with the following structure:
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
                
                Please do it for the following: {previous_task}
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
            dependencies=[],
            validation_type="json"
        )