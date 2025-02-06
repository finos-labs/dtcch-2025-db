import pandas as pd
import json

from pydantic import BaseModel, ValidationError, ConfigDict

from agents.agent_risk_assessment import AgentRiskAssessment
from db_functions import kyc_process_insert_risks

class RiskAssessment(BaseModel):
    model_config = ConfigDict(strict=True)
    risk_tier: str
    risk_summary: str

class RiskHandler:

    def __init__(self):
        """Initialize the risk handler."""
        self.agent_risk = AgentRiskAssessment()

    def extract_client_formation(self, kyc_id: int, data_point: str) -> str:
        # TODO: Pulkit call the db client table to extract the client information TBD
        dummy_client_and_background_check_information = "John Smith is a 42-year-old entrepreneur originally from London, currently residing in Dubai. He holds British citizenship and possesses a valid UAE residency visa. His primary source of income comes from his investment firm, which specializes in real estate and international trade. John has multiple bank accounts in the UK and UAE and frequently conducts high-value transactions, particularly in foreign currencies. His identification documents include a valid British passport and an Emirates ID. He maintains an active phone number registered in the UAE and uses an official business email for communications. His proof of address includes recent utility bills and a tenancy contract for his Dubai residence. John has no known political exposure but has business dealings in high-risk jurisdictions, which require enhanced due diligence."
        dummy_client_and_background_check_information = dummy_client_and_background_check_information + """
                John Doe (aka J. Doe)
        128 Shadow Lane
        Darkwood, DW 45678
        john.doe@example.com (electronic mail)
        +1 (555) 789-1234 (telephone, contact number)
        February 5, 2025
        
        Shoreline Bank
        4456 Integrity Ave
        Banktown, BK 98765
        
        Subject: OUTRAGE OVER UNJUSTIFIED ACCOUNT RESTRICTIONS
        
        Dear Mr. Smith,
        
        This situation is absolutely unacceptable. The audacity of Shoreline Bank to impose these baseless restrictions.
        
        I am well aware that my transactions have been flagged, but this level of scrutiny is nothing more than harassment.
        
        As for our beneficial ownership structure, we have already taken the necessary steps to ensure that past issues.
        
        This needs to be resolved immediately. The continued delays and restrictions are causing irreparable harm.
        
        This is your final warning. Fix this now.
        
        Sincerely,
        
        John Doe
        Managing Director
        Phantom Enterprises
        128 Shadow Lane
        Darkwood, DW 45678
        john.doe@example.com
        +1 (555) 789-1234
        Successfully validated the risk assessment: {'risk_tier': 'High', 'risk_summary': "Multiple high-risk factors identified: 1) Involvement in real estate funds and international trade which are high-risk sectors for money laundering, 2) Residence in UAE while maintaining UK accounts indicates potential cross-border complexity, 3) Frequent high-value transactions in foreign currencies, 4) Business dealings in high-risk jurisdictions, 5) Complex business structure involving multiple jurisdictions, 6) Real estate investment activities which involve significant amounts of cash transactions. The client's profile shows geographical risk due to operations in Dubai while maintaining UK presence, structural risk due to multiple bank accounts across jurisdictions, and business risk due to involvement in high-risk sectors. While proper identification documents are present, the nature of business activities and jurisdictional exposure necessitate enhanced monitoring and due diligence measures."}
"""
        return dummy_client_and_background_check_information

    def risk_csv_read(self, path: str) -> str:
        df = pd.read_csv(path)
        return df.to_json(orient='records')

    def risk_assessment(self, path_risk: str, kyc_id: int, data_point: str):
        """Process extracted text evidence and perform risk assessment."""

        client_complete_profile = self.extract_client_formation(kyc_id, data_point)
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



        # TODO: insert into data base
        ##kyc_process_insert_risks(kyc_id)
        # insert risk_client into kyc_process table,using kyc_id: int

