import json

from typing import List, Dict, Union
from pydantic import BaseModel, ConfigDict, ValidationError

from crew import Agent, Task

class AgentExtractVariables(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the variables extractor agent with AWS Bedrock client."""
        super().__init__("", "", "")
        self.bedrock_client = bedrock_client or self._init_bedrock_client()
    
    def _create_variables_task(self, action, quote, variables: Dict[str, str]) -> Task:
        """Extract variables using AWS Bedrock."""
        # Prepare the prompt
        prompt = f"""Analyze the following action (aka KYC requirement) and quote from a policy document, and provide, without adding any verbosity, but returning just the JSON object:
        1. The variable role of the party the action relates to. Select one ore more values from {variables['role']}.
        2. The variable due diligence level that the action relates to. Select one or more values from {variables['due_diligence_level']}
        3. The variable type of business being conducted with the client. Select one or more values from {variables['business_type']}
        4. The variable entity type the action relates to. Select one or more values from {variables['entity_type']}
        5. The variable internal evidence. It should always be "internal documents"
        6. The variable public evidence. Select one or more values from {variables['public_evidence']}
        5. The variable client evidence. Select one or more values from {variables['non_public_evidence']}

        
        Action: {action}
        Quote: {quote}
        
        Additional Context: you should all applicable values for each variable from the provided list of available ones.
        
        Please format your response as JSON with the following structure:
        {{
            "role": ["role1", "role2", ...],
            "due_diligence_level": ["due_diligence_level1", "due_diligence_level2", ...]
            "business_type": ["business_type1", "business_type2", ...]
            "entity_type": ["entity_type1", "entity_type2", ...],
            "internal_evidence": ["Internal documents"],
            "public_evidence": ["evidence1", "evidence2", ...],
            "client_evidence": ["evidence1", "evidence2", ...]
        }}
        """

        task = Task(
            description=prompt,
            agent_role="agent_validator",
            expected_output="JSON of required variables"
        )

        return task
        
        # response = self.invoke_bedrock(prompt)
        # TODO: execute task in the main instead of invoking bedrock
        # response = self.execute_task(Task())

        class VariablesOutput(BaseModel):
            model_config = ConfigDict(strict=True)
            role: List[str]
            due_diligence_level: List[str]
            business_type: List[str]
            entity_type: List[str]
            internal_evidence: List[str]
            public_evidence: List[str]
            client_evidence: List[str]

        try:
            VariablesOutput.model_validate_json(response) 
            return json.loads(response) 
        except ValidationError as e:
            print(e)

    def _analyze_quote_and_action(self, action, quote, variables: Dict[str, str]) -> Dict[str, str]:
        """Extract variables using AWS Bedrock."""
        # Prepare the prompt
        prompt = f"""Analyze the following action (aka KYC requirement) and quote from a policy document, and provide, without adding any verbosity, but returning just the JSON object:
        1. The variable role of the party the action relates to. Select one ore more values from {variables['role']}.
        2. The variable due diligence level that the action relates to. Select one or more values from {variables['due_diligence_level']}
        3. The variable type of business being conducted with the client. Select one or more values from {variables['business_type']}
        4. The variable entity type the action relates to. Select one or more values from {variables['entity_type']}
        5. The variable internal evidence. It should always be "internal documents"
        6. The variable public evidence. Select one or more values from {variables['public_evidence']}
        5. The variable client evidence. Select one or more values from {variables['non_public_evidence']}

        
        Action: {action}
        Quote: {quote}
        
        Additional Context: you should all applicable values for each variable from the provided list of available ones.
        
        Please format your response as JSON with the following structure:
        {{
            "role": ["role1", "role2", ...],
            "due_diligence_level": ["due_diligence_level1", "due_diligence_level2", ...]
            "business_type": ["business_type1", "business_type2", ...]
            "entity_type": ["entity_type1", "entity_type2", ...],
            "internal_evidence": ["Internal documents"],
            "public_evidence": ["evidence1", "evidence2", ...],
            "client_evidence": ["evidence1", "evidence2", ...]
        }}
        """
        
        response = self.invoke_bedrock(prompt)
        # TODO: execute task in the main instead of invoking bedrock
        # response = self.execute_task(Task())

        class VariablesOutput(BaseModel):
            model_config = ConfigDict(strict=True)
            role: List[str]
            due_diligence_level: List[str]
            business_type: List[str]
            entity_type: List[str]
            internal_evidence: List[str]
            public_evidence: List[str]
            client_evidence: List[str]

        try:
            VariablesOutput.model_validate_json(response) 
            return json.loads(response) 
        except ValidationError as e:
            print(e)
            return None