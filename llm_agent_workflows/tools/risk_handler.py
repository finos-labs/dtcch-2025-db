import pandas as pd
import json

from pydantic import BaseModel, ValidationError, ConfigDict

from agents.agent_risk_assessment import AgentRiskAssessment
from tools.db_functions import kyc_process_insert_risks

class RiskAssessment(BaseModel):
    model_config = ConfigDict(strict=True)
    risk_tier: str
    risk_summary: str

class RiskHandler:

    def __init__(self):
        """Initialize the risk handler."""
        self.agent_risk = AgentRiskAssessment()

    def extract_client_formation(self, kyc_id: int) -> str:
        # TODO: Pulkit call the db client table to extract the client information TBD
        
        dummy_client_and_background_check_information = "John Smith is a 42-year-old entrepreneur originally from London, currently residing in Dubai. He holds British citizenship and possesses a valid UAE residency visa. His primary source of income comes from his investment firm, which specializes in real estate and international trade. John has multiple bank accounts in the UK and UAE and frequently conducts high-value transactions, particularly in foreign currencies. His identification documents include a valid British passport and an Emirates ID. He maintains an active phone number registered in the UAE and uses an official business email for communications. His proof of address includes recent utility bills and a tenancy contract for his Dubai residence. John has no known political exposure but has business dealings in high-risk jurisdictions, which require enhanced due diligence."
        # TODO: check all actions with this kyc_id
        dummy_all_evidence_from_kyc_process = ""
        return dummy_client_and_background_check_information + dummy_all_evidence_from_kyc_process

    def risk_csv_read(self, path: str) -> str:
        df = pd.read_csv(path)
        return df.to_json(orient='records')

    def risk_assessment(self, path_risk: str, kyc_id: int):
        """Process extracted text evidence and perform risk assessment."""

        client_complete_profile = self.extract_client_formation(kyc_id)
        risks = self.risk_csv_read(path_risk)

        # Perform risk assessment based on risks and complete profile
        risk_assessment_string = self.agent_risk._risk_assessment(risks, client_complete_profile)
        try:
            RiskAssessment.model_validate_json(risk_assessment_string)
            risk_assessment = json.loads(risk_assessment_string)
            print("Successfully validated the risk assessment:", risk_assessment)
            kyc_process_insert_risks(risk_assessment, kyc_id)
        except ValidationError as e:
            print(e)