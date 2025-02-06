from crew import Agent, Task


class AgentKYCBackgroundCheckOps(Agent):

    def __init__(self, client_internal_data, client_required_data_points_variables, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        # Set required attributes for agent
        self.role = "kyc_ops_background_check_specialist"
        self.goal = ""  # Independent for every task
        self.backstory = "With over 10 years of experience in financial compliance, the KYC Compliance Operations officer has worked with global financial institutions, helping them align with international AML/KYC regulations like FATF, FINCEN, and GDPR. They use a structured approach to ensure data accuracy and compliance integrity."
        self.client_internal_data = client_internal_data
        self.client_required_data_points_variables = client_required_data_points_variables
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def task_background_check(self) -> Task:
        """Task: Compare the existing internal document client information with the required data points and complete the profile"""
        self.goal = "Convert section to individual sentences"
        
        data_points_variable_text = "\n".join(
            [f"{i+1}. {point[0]}:{point[1]}" for i, point in enumerate(self.client_required_data_points_variables)]
        )
        
        return Task(
        description = f"""I will give you several data points in a list format along with variables associated with this data point and these variables are role(list), due_diligence_level(list), business_type(list), entity_type(list).
        These variables are basically the attributes for this particular data point and you need to verify which variables are actually relevant for a particular data point.
        Once you have found the relevant variables for the data point, you need to check if any information related to the variable + data point is actually present in the context document and extract the value for that data point. I will provide you with this client related information document to check in the context. 
        The data points and their corresponding variables are these following - {data_points_variable_text}""",
        agent_role = "kyc_ops_background_check_specialist",
        expected_output = """Provide me only and only with a json formatted output consisting of the mapping between data points and the actual value that you found. 
        After evaluating all the variables for a corresponding data point, just give me a single one to one mapping between the data point and exact the value/information regarding the data point that you found in the document.
        If you did not find the value, just map the data point to empty in the json""",
        context=self.client_internal_data,
        dependencies=[]   
    )
