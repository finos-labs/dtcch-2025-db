import argparse
from crew import Crew
from pydantic import BaseModel, ConfigDict

from agents.agent_kyc_background_check_specialist import AgentKYCBackgroundCheckOps
from llm_agent_workflows.tools import EvidenceHandler, RiskHandler
from tools.db_functions import fetch_all_data_points_variables, fetch_client_data_file_path


class SectionOutput(BaseModel):
    model_config = ConfigDict(strict=True)
    quote: str
    action_detected: bool
    action: str
    data_point: str

def main():
    parser = argparse.ArgumentParser(description='Extract KYC client and idvariables with AWS Bedrock analysis')

    parser.add_argument('--kyc_id', '-kycid', required=True, help='Current process kyc ID')
    parser.add_argument('--client_id', '-cid', required=True, help='ID of the client to be processed')
    parser.add_argument('--policy_id', '-pid', required=True, help='ID of the policy to be processed')
    args = parser.parse_args()

    ############ Agent Ops Workflow 2 Begins
    client_data_file_path = fetch_client_data_file_path(client_id=args.client_id)

    # Read internal client data for performing background check
    with open(client_data_file_path, "r", encoding="utf-8") as file:
        client_internal_data = file.read()

    # Fetch all required data points and corresponding variables from database
    client_required_data_points_variables = fetch_all_data_points_variables(kyc_id=args.kyc_id)

    agent_kyc_ops = AgentKYCBackgroundCheckOps(client_internal_data=client_internal_data,
                                               client_required_data_points_variables=client_required_data_points_variables)

    # Create a crew for kyc ops
    crew_ops = Crew(
        agents=[agent_kyc_ops],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=False
    )

    # Go through all data points and check each one by one in internal client data document
    background_check_task = agent_kyc_ops.task_background_check()

    # Starting background check workflow
    print("\nStarting background check...\n")
    results = crew_ops.execute_tasks([background_check_task])
    pass

    RISK_PATH = "tools/input/risks/risks.csv"
    evidence_handler = EvidenceHandler()
    risk_handler = RiskHandler()

    # TODO: this will be passed when this is triggered
    kyc_id = 2
    data_point = "Transaction Monitoring"
    image_path = "tools/input/examples_evidence/evidence_driving_licence.jpeg"

    # the evidence will process the image and extract the text and insert it in the db
    evidence_handler.process_evidence(image_path, kyc_id, data_point)
    risk_handler.risk_assessment(RISK_PATH, kyc_id, data_point)

if __name__ == "__main__":
    main()