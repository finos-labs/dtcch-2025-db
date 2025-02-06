from crew import Agent

class AgentEvidence(Agent):
    def __init__(self, bedrock_client=None):
        """Initialize the PDF Handler with AWS Bedrock client."""
        super().__init__()
        self.bedrock_client = bedrock_client or self._init_bedrock_client()

    def _evidence_clean(self, evidence: str) -> str:
        """Process extracted text evidence."""

        prompt = f"""
            You are a highly intelligent assistant designed to clean and format extracted text. The text comes from OCR (Optical Character Recognition) results and may contain raw content. Your job is to:
            
            1. Clean the text by removing any unnecessary characters, extra spaces, line breaks, or other noise.
            2. Add synonyms to key KYC information.
            3. Remove any irrelevant information such as extra punctuation or broken text.
            4. The output should be only the cleaned text, no additional comments.
            
            Here is the text extracted from the image using OCR:
            {evidence}
        """

        response = self.invoke_bedrock(prompt)

        return response
