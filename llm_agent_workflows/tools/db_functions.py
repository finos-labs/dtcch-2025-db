# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os
# from alchemy_models import KycOps

# load_dotenv()

# # Define PostgreSQL connection URL
# DATABASE_URL = os.getenv("DATABASE_URL")

# # Create the database engine
# engine = create_engine(DATABASE_URL)

# # Create a session factory
# SessionLocal = sessionmaker(bind=engine)

# # Create a session
# session = SessionLocal()

# # Function to insert data into kyc_ops table
# def update_action(payload):
    
#     new_entry = Ky
    
#     new_entry = KycOps(ops_name=ops_name, ops_designation=ops_designation)
#     session.add(new_entry)  # Add to session
#     session.commit()  # Commit transaction
#     print(f"Added {ops_name} as {ops_designation} to the database.")

# # Example usage
# payload = [
# {
#         "quote": "Identify the Natural Person Client Senior Manager's residential address",
#         "action_detected": True,
#         "action": "Identify residential address",
#         "data_point": "Residential Address",
#         "role": ["Organisation Senior Management"],
#         "due_diligence_level": ["Client Due Diligence"],
#         "business_type": ["Other Business Type"],
#         "entity_type": ["Private Individual"],
#         "internal_evidence": ["Client Data System", "Internal documents and file notes"],
#         "public_evidence": ["Credit Reference Agency", "Internet searches"],
#         "client_evidence": ["Utility Bill", "Bank statement", "Council tax letter", "Driving licence", "Document issued by public sector or local authority"]
#     },
# ]

# update_action(payload)
