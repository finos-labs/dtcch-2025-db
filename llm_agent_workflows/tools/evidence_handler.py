import pytesseract
from PIL import Image

from agents.agent_evidence_process import AgentEvidence


class EvidenceHandler:

    def __init__(self):
        """Initialize the evidence handler."""
        self.agent_evidence = AgentEvidence()

    @staticmethod
    def extract_text_ocr(image_path: str) -> str:
        """Extract text from an image using Tesseract OCR."""

        # Set the tesseract path
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
        # Open the image using Pillow
        image = Image.open(image_path)
        # Pass the image to pytesseract for text extraction
        text = pytesseract.image_to_string(image)
        print("Extracted Text:", text)
        return text

    def _data_clean_and_insert_in_db(self, text_extracted_ocr: str, kyc_id: int, data_point: str):
        """Clean and format extracted text and insert into the database."""

        # Clean and format the extracted text
        cleaned_text = self.agent_evidence._evidence_clean(text_extracted_ocr)
        print ("Cleaned Text:", cleaned_text)

        # TODO: Insert the cleaned text into the database
        # insert clean evidence in evidence type into actions
        # using kyc_id: int, data_point: str in action table

    def process_evidence(self, image_path: str, kyc_id: int, data_point: str):
        """Process extracted text evidence and insert into the database."""

        text_extracted_ocr = self.extract_text_ocr(image_path)
        self._data_clean_and_insert_in_db(text_extracted_ocr, kyc_id, data_point)
