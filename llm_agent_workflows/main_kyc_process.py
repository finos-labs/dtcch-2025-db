import argparse
from crew import Crew
from pydantic import BaseModel, ConfigDict
import uuid

from agents.agent_kyc_background_check_specialist import AgentKYCBackgroundCheckOps
from tools.trigger_mails import request_docs
from tools.db_functions import fetch_all_data_points_variables, update_action_in_progress, fetch_client_data_file_path, fetch_processed_policy_json, store_evidence_uuid, update_flow_status


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
    
    update_flow_status(args.kyc_id, "IN PROGRESS")

    #Reading policy JSON
    process_policy_dict = fetch_processed_policy_json(args.policy_id) 
    #Adding process policy JSON to actions table
    update_action_in_progress(process_policy_dict, args.kyc_id)

 
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
        verbose=True
    )
 
    # Go through all data points and check each one by one in internal client data document
    background_check_task = agent_kyc_ops.task_background_check()
 
    # Starting background check workflow
    print("\nStarting background check...\n")
    results = crew_ops.execute_tasks([background_check_task])
    result_json = list(results.values())[0]
     
    unique_evidence_id = str(uuid.uuid4())
    
    store_evidence_uuid(unique_evidence_id, args.kyc_id)
    
    print("\nTriggering client doc request mail...\n")
    #Requesting docs from clients
    request_docs(string_id=unique_evidence_id, 
                 callback_url = "some callback", 
                 email_text=f"Please upload documents for KYC: https://dtcch-2025-db.sibnick.men/backend2/static/upload.html?uid={unique_evidence_id}",
                 email="pulkitkhera97@gmail.com",
                 doc_types = ["Passport"]
                 )


if __name__ == "__main__":
    main()
