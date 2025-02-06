import time
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Extract KYC variables with AWS Bedrock analysis')
        parser.add_argument('--kyc_id', '-kycid', required=True, help='Current process kyc ID')
        parser.add_argument('--policy_id', '-pid', required=True, help='ID of the policy to be processed')
        parser.add_argument('--client_id', '-cid', required=True, help='ID of the client to be processed')
        parser.add_argument('--pages', '-pg', help='Page range (e.g., "1-20" or "1,2,3")')
        parser.add_argument('--variable_references_path', '-v',
                           help='Path to the directory containing CSV files, one for each variable with possible values')
        args = parser.parse_args()
        print(f"Arguments received: {args.kyc_id} {args.policy_id} {args.client_id}")

        time.sleep(100)  # Simulate a delay
        print(f"KYC {args.kyc_id} finished!")
    except Exception as e:
        print(f"error in KYC {e}")

if __name__ == "__main__":
    main()