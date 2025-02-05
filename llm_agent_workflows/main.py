from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_kyc_review_policy import AgentKYCReviewPolicy
from pdfplumber import PDF
from pydantic import BaseModel, ConfigDict, ValidationError
from tools.variables_extractor import VariablesExtractor
from agents.agent_extract_variables import AgentExtractVariables
import json
import argparse
import time
import os

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
    parser.add_argument('--output', '-o',
                       help='Output JSON file path (default: ./output/processed_policy_TIMESTAMP.json)')
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

    # TODO: here we should call a function like this:
    # pdf_handler.some_function(pdf_policy_path) -> filename: str, processed_policy_sections: List(ProcessedPolicySection)
    # where:
    # class ProcessedPolicySection():
    #   policy_num: int
    #   labels: List[str]   ## NOT SURE if needed, probably not
    #   section: str        ## Must be something like: Senior management of any enterprise is responsible for managing its business effectively. Certain obligations are placed on all firms subject to the ML Regulations, POCA and the Terrorism Act and under the UK financial sanctions regimes - fulfilling these responsibilities falls to senior management as a whole. These obligations are summarised in Appendix II.
    # Then we loop through every processed_policy_sections, and we extract from the sections the single sentences
    # Inside this loop we also loop through all the sentences, like we do in the following code
    # The final result will be a big json file with the filename of the policy as a field and then a "actions" field, which will contain each action with variables and a reference to the section of the policy
    
    # example of processed section, provided by agent form Matthew
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

    # TODO: do this outside the for loop we will add, adding to the json the filename
    # if vars.output_path is None:
    #         timestamp = time.strftime('%Y%m%d_%H%M%S')
    #         output_path = f"./output/processed_policy_{timestamp}.json"
    # # Create output directory if it doesn't exist
    # os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # with open(output_path, 'w') as output_file:
    #     json.dump(validate_data_point, output_file)
    

if __name__ == "__main__":
    main()
