import pytesseract
from PIL import Image

from agents.agent_evidence_process import AgentEvidence
from .db_functions import actions_insert_processed_evidence, kyc_process_check_status_actions

RISK_PATH = "tools/input/risks/risks.csv"

class EvidenceHandler:

    def __init__(self):
        """Initialize the evidence handler."""
        self.agent_evidence = AgentEvidence()

    @staticmethod
    def extract_text_ocr(image_path: str) -> str:
        """Extract text from an image using Tesseract OCR."""

        # Set the tesseract path
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
        # Open the image using Pillow
        image = Image.open(image_path)
        # Pass the image to pytesseract for text extraction
        text = pytesseract.image_to_string(image)
        print("Extracted Text:", text)
        return text

    def _data_clean_and_insert_in_db(self, text_extracted_ocr: str, uuid: str):
        """Clean and format extracted text and insert into the database."""

        cleaned_text = self.agent_evidence._evidence_clean(text_extracted_ocr)
        print ("Cleaned Text:", cleaned_text)
        actions_insert_processed_evidence(cleaned_text, uuid)

    def process_evidence(self, image_path: str, uuid: str):
        """Process extracted text evidence and insert into the database."""

        text_extracted_ocr = self.extract_text_ocr(image_path)
        self._data_clean_and_insert_in_db(text_extracted_ocr, uuid)

        # get kyc_id from action from uuid, then check the status of the kyc_id related actions, and if status all done then update kyc_process status to done
        kyc_process_id = kyc_process_check_status_actions(uuid)

        # the evidence will process the image and extract the text and insert it in the db
        if kyc_process_id:
            from tools import RiskHandler

            risk_handler = RiskHandler()
            risk_handler.risk_assessment(RISK_PATH, kyc_process_id)

