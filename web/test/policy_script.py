import time
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Process policy')
        parser.add_argument('--policy_id', '-pid', required=True, help='ID of the policy to be processed')
        args = parser.parse_args()
        print(f"Arguments received: {args.policy_id}")

        time.sleep(50)  # Simulate a delay
        print(f"Policy processing {args.policy_id} finished!")
    except Exception as e:
        print(f"error in Policy processing {e}")

if __name__ == "__main__":
    main()