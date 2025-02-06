import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from alchemy_models import Actions, KycProcess

load_dotenv()

# Define PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Create a session
session = SessionLocal()

# Function to insert data into kyc_ops table
def update_action_in_progress(payload):
    
    entry_json_obj = json.loads(payload)
    
    for row in entry_json_obj:
        db_entry = Actions(
            kyc_id = 1,
            data_point = row['data_point'],
            latest_action_activity = "",
            business_type = row['business_type'],
            due_diligence_level = row['due_diligence_level'],
            entity_type = row['entity_type'],
            role = row['role'],
            policy_quote = row['quote'],
            internal_evidence_source = row['internal_evidence'],
            external_evidence_source = row['public_evidence'],
            client_evidence_source = row['client_evidence'],
            action_description = row['action']            
        )
        session.add(db_entry)
    session.commit()
    print(f"Added output action info to the database.")

def actions_insert_processed_evidence(evidence, kyc_id, data_point):
    try:
        session.query(Actions).filter(kyc_id=kyc_id, data_point=data_point).update({Actions.client_evidence_summary:evidence})
        session.commit()
        print ("Inserted Evidence extract in the database.")
    except Exception as e:
        print(f"Error inserting evidence in the database: {str(e)}")
        session.rollback()

def actions_fetch_processed_evidence(evidence, kyc_id, data_point):
    try:
        session.query(Actions).filter(kyc_id=kyc_id, data_point=data_point).update({Actions.client_evidence_summary:evidence})
        session.commit()
        print ("Inserted Evidence extract in the database.")
    except Exception as e:
        print(f"Error inserting evidence in the database: {str(e)}")
        session.rollback()

    # Verifying the update (optional)
    updated_action = session.query(Actions).filter(kyc_id=kyc_id, data_point=data_point).first()
    print(f"Updated Evidence Summary: {updated_action.client_evidence_summary}")

def kyc_process_insert_risks(risk_tier, risk_summary, kyc_id):
    try:
        session.query(KycProcess).filter(kyc_id=kyc_id).update({KycProcess.risk_tier:risk_tier, KycProcess.risk_assessment_summary:risk_summary})
        session.commit()
        print ("Inserted Evidence extract in the database.")
    except Exception as e:
        print(f"Error inserting evidence in the database: {str(e)}")
        session.rollback()

# Example usage
payload = """[
    {
        "quote": "Identify the Natural Person Client Senior Manager's residential address",
        "action_detected": true,
        "action": "Identify residential address",
        "data_point": "Residential Address",
        "role": ["Organisation Senior Management"],
        "due_diligence_level": ["Client Due Diligence"],
        "business_type": ["Other Business Type"],
        "entity_type": ["Private Individual"],
        "internal_evidence": ["Client Data System", "Internal documents and file notes"],
        "public_evidence": ["Credit Reference Agency", "Internet searches"],
        "client_evidence": [
            "Utility Bill",
            "Bank statement",
            "Council tax letter",
            "Driving licence",
            "Document issued by public sector or local authority"
        ]
    }
]
"""

update_action_in_progress(payload)
