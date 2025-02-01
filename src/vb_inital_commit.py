# Use the Conversation API to send a text message to Anthropic Claude.
import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(service_name="bedrock-runtime"
                          , region_name="us-west-2"
                            # find the credentials here, https://devx-systems.awsapps.com/start/#/?tab=accounts
                          , aws_access_key_id=""
                          , aws_secret_access_key = ""
                          , aws_session_token = ""
                      )
# Set the model ID, e.g., Claude 3 Haiku.
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"

# Start a conversation with the user message.
user_message = "Describe the purpose of a 'hello world' program in one line."
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)


