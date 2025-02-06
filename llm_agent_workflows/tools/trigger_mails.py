import requests
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_SERVER_URL = os.getenv("MAIL_SERVER_URL")


def request_docs(string_id, callback_url, email_text, email, doc_types):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "string_id": string_id,
        "callback_url": callback_url,
        "email_text": email_text,
        "email": email,
        "doc_types": doc_types
    }

    response = requests.post(MAIL_SERVER_URL, headers=headers, json=payload)
    
    return response.json() if response.status_code == 200 else response.text

# Example usage:
string_id = "UUID"
callback_url = "some callback"
email_text = f"Please upload documents for KYC: https://dtcch-2025-db.sibnick.men/backend2/static/upload.html?uid={string_id}"
email = "someemail@some.domain.com"
doc_types = ["Passport", "Directors list"]

response = request_docs(string_id, callback_url, email_text, email, doc_types)
print(response)
