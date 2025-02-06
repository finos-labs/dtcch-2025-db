import argparse
import json
import pandas as pd
import textdistance as td
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import boto3
from tqdm import tqdm
import pickle
import numbers
from typing import List
import csv

def bedrock_embeddings_prompt(quote):
    return """{
    "anthropic_version": "bedrock-2024-10-22",
    "max_tokens": 2000,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {quote}
                }
            ]
        }
    ],
    "temperature": 0.5,
    "top_p": 0.9
    }"""

def get_bedrock_embeddings(quotes, client, model_id):
    embeddings = []
    for quote in quotes:
        response = client.invoke_model(
            modelId=model_id,
            contentType='application/json',
            body=json.dumps(bedrock_embeddings_prompt(quote))
        )
        embedding = json.loads(response['body'].read())['embedding']
        embeddings.append(embedding)
    return np.array(embeddings)

model_id = "amazon.titan-embed-text-v2:0"

def generate_embeddings(model_id, quotes):
    """
    Generate a vector of embeddings for a text input using Amazon Titan Embeddings G1 - Text on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embedding created by the model and the number of input tokens.
    """

    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

    accept = "application/json"
    content_type = "application/json"

    embeddings = []
    for quote in tqdm(quotes):
        body = json.dumps({
        "inputText": quote,
    })
        try:
            response = bedrock.invoke_model(
                body=body, modelId=model_id, accept=accept, contentType=content_type
            )
            response_body = json.loads(response.get('body').read())
            embeddings.append(response_body['embedding'])
        except Exception as e:
            print(e)

    return embeddings

def compute_similarity(embeddings1, embeddings2):
    return cosine_similarity(embeddings1, embeddings2)

# def lower_strip_str(string: str):
#     return str(string).lower().strip()

# def lower_strip_str_list(strings: List[str]):
#     return (lower_strip_str(string) for string in strings)
def jaccard_similarity_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return td.jaccard(set1, set2)

def field_similarity(golden, actual):
    scores = {}
    for field in golden.keys():
        if field in actual and field is not "quote":
            golden_field = golden[field]
            actual_field = actual[field]
            print("ACTUAL", golden_field)
            print("GOLDEN", actual_field)
            if isinstance(golden_field, list) and isinstance(actual_field, list):
                # normalized_golden = lower_strip_str_list(golden_field)
                # normalized_actual = lower_strip_str_list(actual_field)
                # print(f"Normalized Golden: {normalized_golden}")
                # print(f"Normalized Actual: {normalized_actual}")
                # scores[field] = td.jaccard(golden_field, actual_field)
                scores[field] = jaccard_similarity_list(golden_field, actual_field)
            elif isinstance(golden_field, numbers.Number):
                continue
            elif isinstance(golden_field, list):
                # print("GOLDEN FIELD LIST", golden_field)
                # # scores[field] = td.jaccard.normalized_similarity(str(golden[field]).lower().strip(), str(actual[field]).lower().strip())
                # normalized_golden = lower_strip_str_list(golden_field)
                # normalized_actual = [lower_strip_str(actual_field)]
                # print(f"Normalized Golden: {normalized_golden}")
                # print(f"Normalized Actual: {normalized_actual}")
                # scores[field] = td.jaccard(golden_field, [actual_field])
                scores[field] = jaccard_similarity_list(golden_field, [actual_field])
            elif isinstance(actual_field, list):
                # normalized_golden = [lower_strip_str(golden_field)]
                # normalized_actual = lower_strip_str_list(actual_field)
                # print(f"Normalized Golden: {normalized_golden}")
                # print(f"Normalized Actual: {normalized_actual}")
                # scores[field] = td.jaccard([golden_field], actual_field)
                scores[field] = jaccard_similarity_list([golden_field], actual_field)
            elif isinstance(golden_field, str) and isinstance(actual_field, str):
                # normalized_golden = lower_strip_str(golden_field)
                # normalized_actual = lower_strip_str(actual_field)
                # print(f"Normalized Golden: {normalized_golden}")
                # print(f"Normalized Actual: {normalized_actual}")
                scores[field] = td.jaccard.normalized_similarity(golden_field, actual_field)
            else:
                scores[field] = 0
    return scores

def csv_to_json(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = [row for row in csv_reader]
    return json_data

def main():
    parser = argparse.ArgumentParser(description='KYC policy extractor evaluator')
    parser.add_argument('--golden_output', '-g', required=True, help='Path of the golden CSV dataset for evaluation')
    parser.add_argument('--actual_output', '-a', required=True, help='Path of the actual output from the system')
    args = parser.parse_args()

    with open(args.actual_output) as f:
        actual_outputs = json.load(f)
    output_quotes = [actual_output['quote'] for actual_output in actual_outputs]
    output_headers = actual_outputs[0].keys()

    # golden_data = pd.read_csv(args.golden_output, on_bad_lines='skip')
    # golden_data = golden_data[[col for col in golden_data.columns if col in output_headers]]
    # golden_data_json = f"[{(json.dumps(d) for d in csv.DictReader(open(args.golden_output)))}]"
    # golden_data = json.loads(golden_data_json)
    # golden_data = golden_data[[col for col in golden_data.columns if col in output_headers]]
    golden_data = csv_to_json(args.golden_output)
    # golden_quotes = [g['quote'].tolist() for g in golden_data]
    golden_quotes = [row['quote'] for row in golden_data]

    print("Generating embeddings for golden dataset quotes")
    # golden_embeddings = generate_embeddings(model_id, golden_quotes)
    # with open("golden_embeddings", 'wb') as f:
    #     pickle.dump(golden_embeddings, f)
    with open("golden_embeddings", 'rb') as f:
        golden_embeddings = pickle.load(f)
    print("Generating embeddings for output dataset quotes")
    # actual_embeddings = generate_embeddings(model_id, output_quotes)
    # with open("actual_embeddings", 'wb') as f:
    #     pickle.dump(actual_embeddings, f)
    with open("actual_embeddings", 'rb') as f:
        actual_embeddings = pickle.load(f)

    similarity_matrix = compute_similarity(actual_embeddings, golden_embeddings)

    for i, actual_output in enumerate(actual_outputs):
        most_similar_index = np.argmax(similarity_matrix[i])
        most_similar_golden = golden_data[most_similar_index]
        field_scores = field_similarity(actual_output, most_similar_golden)
        print(f"Actual Quote: {output_quotes[i]}")
        print(f"Most Similar Golden Quote: {most_similar_golden['quote']}")
        print(f"Field Scores: {field_scores}")

if __name__ == "__main__":
    main()