from dotenv import load_dotenv
from crew import Task, Crew
from agents.agent_kyc_review_policy import AgentKYCReviewPolicy
from pdfplumber import PDF
from pydantic import BaseModel, ConfigDict, ValidationError
from tools.variables_extractor import VariablesExtractor
from agents.agent_extract_variables import AgentExtractVariables
from tools.pdf_handler_type import PDFHandlerType
import json
import argparse
import fitz
from pathlib import Path
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
    parser.add_argument('--policy_pdf', '-p', required=True, help='Path to the PDF file')
    parser.add_argument('--pages', '-pg', help='Page range (e.g., "1-20" or "1,2,3")')
    parser.add_argument('--variable_references_path', '-v',
                       required=True,
                       help='Path to the directory containing CSV files, one for each variable with possible values')
    parser.add_argument('--output', '-o',
                       help='Output JSON file path (default: ./output/processed_policy_TIMESTAMP.json)')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    variables_options = VariablesExtractor().extract_variable_values(args.variable_references_path)
    policyHandler = PDFHandlerType()
    agent_kyc_review_policy = AgentKYCReviewPolicy()
    agent_extract_variables = AgentExtractVariables()
    pdf_path = args.policy_pdf

    # Parse page range if provided
    pages = None
    if args.pages:
        if '-' in args.pages:
            start, end = map(int, args.pages.split('-'))
            pages = (start, end)
        else:
            pages = [int(p) for p in args.pages.split(',')]

    # Create a crew with the kyc review policy agent
    crew = Crew(
        agents=[agent_kyc_review_policy],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=False
    )

    try:
        print(f"Opening PDF file: {pdf_path}")
        doc = fitz.open(pdf_path)
        pdf_name = Path(pdf_path).name
        total_pages = len(doc)
        print(f"Total pages in PDF: {total_pages}")
        # Determine which pages to process
        if pages is None:
            pages_to_process = range(total_pages)
        elif isinstance(pages, tuple):
            start, end = pages
            pages_to_process = range(start - 1, min(end, total_pages))
        else:
            pages_to_process = [p - 1 for p in pages if 1 <= p <= total_pages]
        result = []
        for page_num in pages_to_process:
            print(f"Processing page {page_num + 1}")
            page = doc[page_num]
            # Extract text from the page
            page_text = page.get_text()
            if not page_text.strip():
                print(f"No text found on page {page_num + 1}")
                continue
            # Analyze the page content
            sentences = policyHandler._analyze_page_with_llm(page_text, page_num + 1)
            
            # Add metadata to each sentence
            for i in range(len(sentences)):
                sentences[i]["pdf_name"] = pdf_name
                # validate_data_point = []
                sentence = sentences[i]["sentence"]
                task_action_to_data_point = agent_kyc_review_policy.task_actions_to_data_points(previous_task=sentence)
                tasks = [task_action_to_data_point]
                print("\nStarting Content Creation Workflow...\n")
                crew_results = crew.execute_tasks(tasks)
                list_crew_results = list(crew_results.items())
                action_result = list_crew_results[i][1]
                try:
                    if action_result == '{"action_detected": False}' or action_result == '{"action_detected": false}':
                        pass
                    else:
                        SectionOutput.model_validate_json(action_result)
                        dict_result = json.loads(action_result)
                        variables = agent_extract_variables._analyze_quote_and_action(dict_result['action'], dict_result['quote'], variables_options)
                        dict_result.update(variables)
                        # validate_data_point.append(dict_result)
                        sentences[i].pop("sentence")
                        sentences[i].update(dict_result)
                except ValidationError as e:
                    print(e)

                # print(json.dumps(validate_data_point))
                
            result.append(sentences)
        print(json.dumps(result)) 

    except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            
    section = ["Standard identification procedures will usually apply.",#
               "In some cases, the firm holding the existing account may be willing to confirm the identity of the account holder to the new firm, and to provide evidence of the identification checks carried out. ",
               "Care will need to be exercised by the receiving firm to be satisfied that the previous verification procedures provide an appropriate level of assurance for the new account, which may have different risk characteristics from the one held with the other firm."]

    

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
