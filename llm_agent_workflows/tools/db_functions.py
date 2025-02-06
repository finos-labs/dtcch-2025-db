import os
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .alchemy_models import Actions, Policy, Client


import json

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
def update_action_in_progress(payload, kyc_id):

    for row in payload:
        db_entry = Actions(
            kyc_id = kyc_id,
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
        if row['action_detected'] and row['type_of_sentence'] == 'KYC Profile Relevant':
            session.add(db_entry)

    try:
        session.commit()
        print(f"Added output action info to the database.")
    except IntegrityError:
        session.rollback()
        print(f"Skipping duplicate entry: {kyc_id}")

def fetch_policy_file_path(policy_id):
    file_path = session.query(Policy).filter_by(policy_id=policy_id).first().policy_file_path
    return file_path

def fetch_client_data_file_path(client_id):
    file_path = session.query(Client).filter_by(client_id=client_id).first().client_info_file_path
    return file_path

def fetch_all_data_points_variables(kyc_id):
    kyc_records = session.query(Actions).filter_by(kyc_id=kyc_id).all()
    data_points_variables = []
    for kyc_record in kyc_records:
        variable_dict = {
            "role": kyc_record.role,
            "due_diligence_level": kyc_record.due_diligence_level,
            "business_type": kyc_record.business_type,
            "entity_type": kyc_record.entity_type
        }
        data_points_variables.append((kyc_record.data_point, variable_dict))
    return data_points_variables

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

def kyc_process_insert_risks(risk_assessment, kyc_id):
    try:
        session.query(KycProcess).filter(kyc_id=kyc_id).update({KycProcess.risk_tier:risk_assessment["risk_tier"], KycProcess.risk_assessment:risk_assessment["risk_summary"]})
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

# update_action_in_progress(payload)
# fetch_policy_file_path(1)
# fetch_client_data_file_path(1)
# fetch_all_data_points(1)