import pandas as pd
from agents.agent_risk_assessment import AgentRiskAssessment


class RiskHandler:

    def __init__(self):
        """Initialize the risk handler."""
        self.agent_risk = AgentRiskAssessment()

    def extract_client_formation(self, kyc_id: int) -> str:
        # TODO: Pulkit call the db client table to extract the client information TBD
        return "client_and background_check_information"

    def risk_csv_read(self, path: str) -> str:
        df = pd.read_csv(path)
        return df.to_json(orient='records')

    def risk_assessment(self, path_risk: str, kyc_id: int, data_point: str):
        """Process extracted text evidence and perform risk assessment."""

        client_profile = self.extract_client_formation(kyc_id)
        risks = self.risk_csv_read(path_risk)
        # Perform risk assessment based on risks and complete profile
        risk_client = self.agent_risk._risk_assessment(risks, client_profile)

        # TODO: add validation of the json (alessio)


        # TODO: insert into data base
        # insert risk_client into kyc_process table,using kyc_id: int

