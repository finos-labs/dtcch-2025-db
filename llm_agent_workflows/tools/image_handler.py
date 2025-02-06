import pytesseract
from PIL import Image

# Set the tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

# Open the image using Pillow
image = Image.open("/llm_agent_workflows/examples_evidence/evidence_driving_licence.jpeg")

# Pass the image to pytesseract for text extraction
text = pytesseract.image_to_string(image)


print("Extracted Text:", text)

# 0. send information to llm to format, not exactly know how
# 1. join information from internal DB and 0. to have the complete profile of the client insert to db
# 2. send this information to the KYC risk agent to check if the profile is risky, with the risk csv
# 2.1 read the db with inserted evidence and send it to the risk agent
# 2.2 once we recive the risk assessment insert it into db,
