from crew import Agent, Task


class AgentKYCBackgroundCheckOps(Agent):

    def __init__(self, client_internal_data, client_required_data_points, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        # Set required attributes for agent
        self.role = "kyc_ops_background_check_specialist"
        self.goal = ""  # Independent for every task
        self.backstory = "With over 10 years of experience in financial compliance, the KYC Compliance Operations officer has worked with global financial institutions, helping them align with international AML/KYC regulations like FATF, FINCEN, and GDPR. They use a structured approach to ensure data accuracy and compliance integrity."
        self.client_internal_data = client_internal_data
        self.client_required_data_points = client_required_data_points
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def task_background_check(self) -> Task:
        """Task: Compare the existing internal document client information with the required data points and complete the profile"""
        self.goal = "Convert section to individual sentences"
        
        return Task(
        description = f"""I will give you several data points in a list format and you need to check if any information related to this data point is actually present in the context document and extract the value for that data point. I will provide you with this document in the context. The data points are these - {self.client_required_data_points}""",
        agent_role = "kyc_ops_background_check_specialist",
        expected_output = "Provide me only and only with a json formatted output consisting of the mapping between data points and the actual value that you found. If you did not find the value, just map it to empty",
        context=self.client_internal_data,
        dependencies=[]   
    )
