import os
import csv
import re
import time
import json

from agents.agent_extract_variables import AgentExtractVariables

class VariablesExtractor:
    def __init__(self):
        """Initialize the JSON Handler with AWS Bedrock client."""
        self.agent = AgentExtractVariables()
    
    def camel_to_snake(self, name):
        """Convert CamelCase to snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    # Quick way of extracting this, will need refactoring
    def extract_variable_values(self, 
                                variable_references_path: str) -> dict[str, str]:
        variable_values = {}
        # List all files in the directory
        for filename in os.listdir(variable_references_path):
            if filename.endswith("Nodes.csv"):
                # Extract the CamelCase part of the filename
                camel_case_name = filename[:-9]  # Remove "Nodes.csv"
                # Convert CamelCase to snake_case
                snake_case_name = self.camel_to_snake(camel_case_name)
                values = []
                # Open the file as CSV and save values
                with (open(os.path.join(variable_references_path, filename))) as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for line in reader:
                        values.append(line[1])
                # Add to the dictionary
                variable_values[snake_case_name] = values
        
        return variable_values
        

    def process_json(self,
                   json_path: str, 
                   output_path: str,
                   variable_references_path) -> None:
        """Process a JSON file and add variables to it."""
        # Generate default output path if not specified
        if output_path is None:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_path = f"./output/variables_{timestamp}.json"
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            # Open JSON
            with (open(json_path)) as f:
                json_input = json.load(f)
            variables_references = self.extract_variable_values(variable_references_path)
            # Process pages and write to JSON
            with open(output_path, 'w') as output_file:
                for i in range(len(json_input)):
                    if json_input[i]["action_detected"]:
                        quote = json_input[i]["quote"]
                        action = json_input[i]["action"]
                        variables = self.agent._analyze_quote_and_action(action, quote, variables_references)
                        if not variables:
                            raise Exception("LLM-returned JSON incorrectly parsed")
                        json_input[i].update(variables)
                        # TODO: add return value to json entry
                json.dump(json_input, output_file)
            print(f"Extraction complete. Output saved to {output_path}")
            
        except Exception as e:
            os.remove(output_path)
            print(f"Error processing JSON: {str(e)}")

def main():
    """Command-line interface for the variables extractor"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract KYC variables with AWS Bedrock analysis')
    
    # TODO: document this
    parser.add_argument('--json_path', '-j',
                       required=True,
                       help='Path to the JSON file containing the action')
    
    parser.add_argument('--variable_references_path', '-v',
                       required=True,
                       help='Path to the directory containing CSV files, one for each variable with possible values')
    
    parser.add_argument('--output', '-o',
                       help='Output JSON file path (default: ../tools/output/variables_TIMESTAMP.json)')
    
    args = parser.parse_args()
    handler = JSONHandler()
    try:
        print(f"Processing JSON: {args.json_path}")
        handler.process_json(args.json_path, args.output, args.variable_references_path)
        
    except Exception as e:
        print(f"Error processing JSON: {str(e)}")

if __name__ == "__main__":
    main()
