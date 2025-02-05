from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_kyc_review_policy import AgentKYCReviewPolicy
from pdfplumber import PDF
from pydantic import BaseModel, ConfigDict, ValidationError
from tools.variables_extractor import VariablesExtractor
from agents.agent_extract_variables import AgentExtractVariables
import json
import argparse

class SectionOutput(BaseModel):
    model_config = ConfigDict(strict=True)
    quote: str
    action_detected: bool
    action: str
    data_point: str

def main():
    parser = argparse.ArgumentParser(description='Extract KYC variables with AWS Bedrock analysis')
    parser.add_argument('--variable_references_path', '-v',
                       required=True,
                       help='Path to the directory containing CSV files, one for each variable with possible values')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    variables_options = VariablesExtractor().extract_variable_values(args.variable_references_path)
    agent_kyc_review_policy = AgentKYCReviewPolicy()
    agent_extract_variables = AgentExtractVariables()

    # Create a crew with these agents
    crew = Crew(
        agents=[agent_kyc_review_policy],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=False
    )

    # example of section, provided by agent form Matthew
    # For Matthew: return a list of policy sections  (e.g. one entry will be Senior management of any enterprise is responsible for managing its business effectively. Certain obligations are placed on all firms subject to the ML Regulations, POCA and the Terrorism Act and under the UK financial sanctions regimes - fulfilling these responsibilities falls to senior management as a whole. These obligations are summarised in Appendix II.)
    # TODO: loop between every returned section
    # TODO: split each section in the loop by sentence (example below)
    section = ["Standard identification procedures will usually apply.",#
               "In some cases, the firm holding the existing account may be willing to confirm the identity of the account holder to the new firm, and to provide evidence of the identification checks carried out. ",
               "Care will need to be exercised by the receiving firm to be satisfied that the previous verification procedures provide an appropriate level of assurance for the new account, which may have different risk characteristics from the one held with the other firm."]

    # Declaration of tasks
    #task_section_to_action = agent_kyc_review_policy.task_section_to_actions(section)
    #task_action_to_data_point = agent_kyc_review_policy.task_actions_to_data_points(previous_task=section)

    # Define tasks with dependencies

    validate_data_point = []
    for i in range(len(section)):
        sect = section[i]
        task_action_to_data_point = agent_kyc_review_policy.task_actions_to_data_points(previous_task=sect)
        tasks = [task_action_to_data_point]
        print("\nStarting Content Creation Workflow...\n")
        results = crew.execute_tasks(tasks)
        list_results = list(results.items())
        result = list_results[i][1]
        try:
            if result == '{"action_detected": False}' or result == '{"action_detected": false}':
                pass
            else:
                SectionOutput.model_validate_json(result)
                dict_result = json.loads(result)
                variables = agent_extract_variables._analyze_quote_and_action(dict_result['action'], dict_result['quote'], variables_options)
                dict_result.update(variables)
                validate_data_point.append(dict_result)
        except ValidationError as e:
            print(e)

    print(json.dumps(validate_data_point))

    

if __name__ == "__main__":
    main()
