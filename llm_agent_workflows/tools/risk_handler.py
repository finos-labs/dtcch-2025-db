import pytesseract
from PIL import Image

from agents.agent_evidence_process import AgentEvidence
from agents.agent_risk_assessment import AgentRiskAssessment


class EvidenceHandler:

    def __init__(self):
        """Initialize the risk hanlder."""
        self.agent_evidence = AgentEvidence()
        self.agent_risk = AgentRiskAssessment()

    def extract_client_formation(self, action_id: int) -> str:
        # TODO: call the db actions table or cleint TBD
        pass

    def risk_csv_read(self, path: str) -> str:
        # TODO: read csv under risk/risks.csv
        pass

    def risk_assessment(self, path_risk: str, action_id: int):
        """Process extracted text evidence and perform risk assessment."""

        client_profile = self.extract_client_formation(action_id)
        risks = self.risk_csv_read(path_risk)
        # Perform risk assessment based on risks and complete profile
        risk_client = self.agent._risk_assessment(risks, client_profile)

        # TODO: add validation of the json (alessio)


        # TODO: insert into data base
        # insert risk_client into action table
