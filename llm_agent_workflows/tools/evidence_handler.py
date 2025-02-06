import pytesseract
from PIL import Image

from agents.agent_evidence_process import AgentEvidence
from db_functions import actions_insert_processed_evidence

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

        cleaned_text = self.agent_evidence._evidence_clean(text_extracted_ocr)
        print ("Cleaned Text:", cleaned_text)
        # TODO: validate if is string
        actions_insert_processed_evidence(cleaned_text)

    def process_evidence(self, image_path: str, kyc_id: int, data_point: str):
        """Process extracted text evidence and insert into the database."""

        #text_extracted_ocr = self.extract_text_ocr(image_path)
        text_extracted_ocr = "Hello, this is a sampl3 of text extracted us1ng Tesseract OCR. The qu3stionnaire includes several qu3stions t0 assess r1sks, including health and saf3ty. Do you w0rk in a high-stress envir0nm3nt? Do you have any pr3vi0us m3dical c0nditions? Pleas3 provide your answ3rs as c0rrectly as possible."
        self._data_clean_and_insert_in_db(text_extracted_ocr, kyc_id, data_point)
