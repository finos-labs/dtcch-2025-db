import pytesseract
from PIL import Image

from agents.agent_risk_assessment import AgentRiskAssessment


class RiskHandler:

    def __init__(self):
        """Initialize the JSON Handler with AWS Bedrock client."""
        self.agent = AgentRiskAssessment()

# Set the tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

# Open the image using Pillow
image = Image.open("/llm_agent_workflows/examples_evidence/evidence_driving_licence.jpeg")

# Pass the image to pytesseract for text extraction
text = pytesseract.image_to_string(image)


print("Extracted Text:", text)


# 0. send information to llm to format,
#   (evidence_clean)
# 1. join information from internal DB and 0. to have the complete profile of the client insert to db
#   insert clean evidence in evidence type into actions
# 2. send this information to the KYC risk agent to check if the profile is risky, with the risk csv
#   fetch all actions (as user profile is complete)
# 2.1 read the db with inserted evidence and send it to the risk agent
#   read csv under risk/risks.csv and send it to risk assesmne
# 2.2 once we receive the risk assessment insert it into db,
