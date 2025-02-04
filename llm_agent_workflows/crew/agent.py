from typing import List, Optional
import boto3
import os
import json
from dotenv import load_dotenv

class Agent:
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List[str]] = None,
        verbose: bool = False
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.client = self._get_bedrock_client()
        
    def _get_bedrock_client(self):
        """Initialize AWS Bedrock client"""
        required_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required AWS credentials: {', '.join(missing_vars)}. "
                           f"Please set these in your .env file.")
        
        try:
            credentials = {
                'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
                'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            }
            
            # Only add session token if it exists
            if os.getenv('AWS_SESSION_TOKEN'):
                credentials['aws_session_token'] = os.getenv('AWS_SESSION_TOKEN')
            
            return boto3.client(
                service_name='bedrock-runtime',
                region_name='us-west-2',  # Changed to us-west-2
                **credentials
            )
        except Exception as e:
            if 'ExpiredTokenException' in str(e):
                raise Exception(
                    "AWS credentials have expired. Please update your AWS credentials in the .env file. "
                    "If you're using temporary credentials, you'll need to refresh them."
                ) from e
            raise Exception(f"Failed to initialize Bedrock client: {str(e)}") from e

    def execute_task(self, task, context=""):
        """Execute a given task using the agent's role and capabilities"""
        try:
            # Validate AWS credentials before making the request
            if not hasattr(self, 'client') or self.client is None:
                self.client = self._get_bedrock_client()
            
            system_prompt = f"""You are an AI agent with the following:
            ROLE: {self.role}
            GOAL: {self.goal}
            BACKSTORY: {self.backstory}
            
            TOOLS AVAILABLE: {', '.join(self.tools) if self.tools else 'No specific tools'}
            
            TASK: {task}
            
            CONTEXT: {context}
            
            Provide your response based on your role and expertise. Be specific and actionable.
            """
            
            response = self.client.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "top_k": 250,
                    "stop_sequences": [],
                    "temperature": 0.7,
                    "top_p": 0.999,
                    "messages": [
                        {
                            "role": "assistant",
                            "content": [{"type": "text", "text": f"I understand my role: {system_prompt}"}]
                        },
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": task}]
                        }
                    ]
                })
            )
            result = json.loads(response['body'].read())['content'][0]['text']
            
            if self.verbose:
                print(f"\n{self.role}'s Response:\n{result}\n")
                
            return result
            
        except Exception as e:
            error_msg = str(e)
            if 'ExpiredTokenException' in error_msg:
                print("\n⚠️  AWS credentials have expired!")
                print("Please update your AWS credentials in the .env file.")
                print("If you're using temporary credentials, you'll need to refresh them.")
            else:
                print(f"\n⚠️  Error executing task: {error_msg}")
            return None
