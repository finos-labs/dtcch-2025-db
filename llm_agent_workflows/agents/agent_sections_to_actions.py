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

    def task_section_to_actions(self) -> Task:
        """Task: Convert document sections into actionable items."""
        section = "Standard identification procedures will usually apply. In some cases, the firm holding the existing account may be willing to confirm the identity of the account holder to the new firm, and to provide evidence of the identification checks carried out. Care will need to be exercised by the receiving firm to be satisfied that the previous verification procedures provide an appropriate level of assurance for the new account, which may have different risk characteristics from the one held with the other firm."
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
    def task_actions_to_data_points(self) -> Task:
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