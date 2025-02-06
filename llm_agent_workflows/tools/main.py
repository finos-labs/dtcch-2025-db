from evidence_handler import EvidenceHandler
from risk_handler import RiskHandler

def main():
    # the risk assessment will read the csv file and perform the risk assessment
    RISK_PATH = "input/risks/risks.csv"
    evidence_handler = EvidenceHandler()
    risk_handler = RiskHandler()

    # TODO: this will be passed when this is triggered
    kyc_id = 2
    data_point = "Transaction Monitoring"
    image_path = "input/examples_evidence/owner_correspondence.jpg"

    # the evidence will process the image and extract the text and insert it in the db
    #evidence_handler.process_evidence(image_path, kyc_id, data_point)
    risk_handler.risk_assessment(RISK_PATH, kyc_id, data_point)

if __name__ == "__main__":
    main()
