from dotenv import load_dotenv
from crew import Crew
from agents.agent_kyc_review_policy import AgentKYCReviewPolicy
from pydantic import BaseModel, ConfigDict, ValidationError
from tools.variables_extractor import VariablesExtractor
from agents.agent_extract_variables import AgentExtractVariables
from tools.pdf_handler_type import PDFHandlerType, Sentence
import json
import argparse
import fitz
from pathlib import Path
import time
import os
from typing import List, Dict

class ActionOutput(BaseModel):
    model_config = ConfigDict(strict=True)
    quote: str
    action_detected: bool
    action: str
    data_point: str

def get_pages_to_process(pages, total_pages):
    if pages:
        if '-' in pages:
            start, end = map(int, pages.split('-'))
            return range(start - 1, min(end, total_pages))
        else:
            pages = [int(p) for p in pages.split(',')]
            return [p - 1 for p in pages if 1 <= p <= total_pages]
    else:
        return range(total_pages)

def process_policy_page(doc: fitz.Document, page_num: int, policy_handler: PDFHandlerType) -> List[Sentence] :
    print(f"Processing page {page_num + 1}")
    page = doc[page_num]
    # Extract text from the page
    page_text = page.get_text()
    if not page_text.strip():
        print(f"No text found on page {page_num + 1}")
        return None
    # Analyze the page content
    return policy_handler._analyze_page_with_llm(page_text, page_num + 1)

def process_sentence(sentence: Sentence, pdf_name: str, agent_kyc_review_policy: AgentKYCReviewPolicy, kyc_reviewer_crew: Crew) -> List[Dict[str, str]]:
    sentence["pdf_name"] = pdf_name
    sentence = sentence["sentence"]
    task_action_to_data_point = agent_kyc_review_policy.task_actions_to_data_points(previous_task=sentence)
    tasks = [task_action_to_data_point]
    crew_results = kyc_reviewer_crew.execute_tasks(tasks)
    return list(crew_results.items())

def convert_crew_output_to_action_output(i: int, crew_output: List[Dict[str, str]]) -> ActionOutput:
    current_result = crew_output[i][1]
    try:
        if current_result == '{"action_detected": False}' or current_result == '{"action_detected": false}':
            return None
        else:
            ActionOutput.model_validate_json(current_result)
            return json.loads(current_result)
    except ValidationError as e:
        print(e)
        return None

def process_action(sentence: Sentence, action_result: ActionOutput, variables_options: Dict[str, str], agent_extract_variables: AgentExtractVariables) -> Dict[str, str]:
    extracted_variables = agent_extract_variables._analyze_quote_and_action(action_result['action'], action_result['quote'], variables_options)
    action_result.update(extracted_variables)
    sentence.pop("sentence")
    sentence.update(action_result)
    return sentence

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
    policy_handler = PDFHandlerType()
    agent_kyc_review_policy = AgentKYCReviewPolicy()
    agent_extract_variables = AgentExtractVariables()

    kyc_reviewer_crew = Crew(
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
        pages_to_process = get_pages_to_process(args.pages, total_pages)
        for page_num in pages_to_process:
            sentences = process_policy_page(doc, page_num, policy_handler)
            if not sentences:
                continue
            for i in range(len(sentences)):
                print(f"Processing sentence {i + 1} of page {page_num + 1}")
                crew_action_from_sentence = process_sentence(sentences[i], pdf_name, agent_kyc_review_policy, kyc_reviewer_crew)
                action_result = convert_crew_output_to_action_output(i, crew_action_from_sentence)
                if not action_result:
                    continue
                final_processed_sentence = process_action(sentences[i], action_result, variables_options, agent_extract_variables)
                result.append(final_processed_sentence)
                print("-------------------------")

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
