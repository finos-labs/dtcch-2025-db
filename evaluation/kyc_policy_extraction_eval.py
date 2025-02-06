from rapidfuzz import process
import pandas as pd
import argparse
import json



def main():
    parser = argparse.ArgumentParser(description='KYC policy extractor evaluator')
    parser.add_argument('--golden_output', '-g', required=True, help='Path of the golden CSV dataset for evaluation')
    parser.add_argument('--actual_output', '-a', required=True, help='Path of the actual output from the system')
    args = parser.parse_args()

    with open(args.actual_output) as f:
        actual_output = json.load(f)

    golden_data = pd.read_csv(args.golden_output)
    quotes = golden_data['quote']
    for i in range(len(quotes)):
        most_similar_list = process.extract(quotes[i], processor=str.lower, score_cutoff=70)
        if len(most_similar_list) > 0:


if __name__ == "__main__":
    main()