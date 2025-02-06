import pytesseract
from PIL import Image

from agents.agent_evidence_process import AgentEvidence


class EvidenceHandler:

    def __init__(self):
        """Initialize the risk handler."""
        self.agent_evidence = AgentEvidence()

    def extract_text_ocr(self, image_path: str) -> str:
        """Extract text from an image using Tesseract OCR."""

        # Set the tesseract path
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
        # Open the image using Pillow
        image = Image.open(image_path)
        # Pass the image to pytesseract for text extraction
        text = pytesseract.image_to_string(image)
        print("Extracted Text:", text)
        return text

    def data_clean_and_insert_in_db(self, text: str) -> str:
        """Clean and format extracted text and insert into the database."""
        # Clean and format the extracted text
        cleaned_text = self.agent._evidence_clean(text)
        # TODO: Insert the cleaned text into the database
        # insert clean evidence in evidence type into actions