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
    parser.add_argument('--output_path', '-o',
                       help='Output JSON file path (default: ./output/<policy_filename>_policy_TIMESTAMP.json)')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    output_path = args.output_path
    pdf_path = args.policy_pdf
    pdf_name = Path(pdf_path).name

    variables_options = VariablesExtractor().extract_variable_values(args.variable_references_path)
    policyHandler = PDFHandlerType()
    agent_kyc_review_policy = AgentKYCReviewPolicy()
    agent_extract_variables = AgentExtractVariables()

    pages = None

    if args.pages:
        if '-' in args.pages:
            start, end = map(int, args.pages.split('-'))
            pages = (start, end)
        else:
            pages = [int(p) for p in args.pages.split(',')]

    crew = Crew(
        agents=[agent_kyc_review_policy],
        max_iterations=1,  # Agents will iterate through tasks twice
        verbose=False
    )

    result = []

    try:
        print(f"Opening PDF file: {pdf_path}")
        doc = fitz.open(pdf_path)
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
                        sentences[i].pop("sentence")
                        sentences[i].update(dict_result)
                        result.append(sentences[i])
                except ValidationError as e:
                    print(e)

    except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            import traceback
            traceback.print_exc()

    if output_path is None:
            policy_name, _ = os.path.splitext(pdf_name)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_path = f"./output/{policy_name}_processed_{timestamp}.json"
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as output_file:
        json.dump(result, output_file)
    

if __name__ == "__main__":
    main()
