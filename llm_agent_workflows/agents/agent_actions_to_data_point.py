import json

from typing import List, Dict, Union

from crew import Agent


class AgentActionsToDataPoints(Agent):

    def __init__(self, bedrock_client=None):
        super().__init__()
        # Set required attributes
        self.role = "kyc_analyst"
        self.goal = "Process actions and requirements to actual data points required from the client to complete KYC"
        self.backstory = "An AI agent that has more than 10 years of experience in completing KYC processes for clients."

        self.bedrock_client = bedrock_client or self._init_bedrock_client()
