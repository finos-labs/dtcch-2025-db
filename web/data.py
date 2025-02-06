from dataclasses import dataclass
from datetime import datetime

from app import db

@dataclass
class Kyc:
    kyc_id: int
    client_id: int
    policy_id: int
    client_name: str
    policy_name: str
    trigger_date: datetime
    status: str
    risk_assessment_summary: str
    risk_tier: str

# Define the REQUEST_FOR_DOCS model
class RequestForDocs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    callback_url = db.Column(db.Text, nullable=False)
    string_id = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@dataclass
class Client(db.Model):
    client_id: int = db.Column(db.Integer, primary_key=True)
    client_name: str = db.Column(db.String(255), nullable=False)
    # client_email = db.Column(db.String(255), nullable=False)

class KycProcess(db.Model):
    kyc_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), nullable=False)
    ops_id = db.Column(db.Integer, db.ForeignKey('kyc_ops.ops_id'), nullable=False)
    initiation_timestamp  = db.Column(db.DateTime, nullable=False)
    overall_status = db.Column(db.String(50), nullable=False)
    risk_assessment_summary = db.Column(db.Text, nullable=False)
    risk_tier = db.Column(db.Text, nullable=False)

@dataclass
class Actions(db.Model):
    __tablename__ = 'actions'
    kyc_id: int = db.Column(db.Integer, db.ForeignKey('kyc_process.kyc_id'))
    latest_action_activity: str = db.Column(db.String(50), nullable=False)
    business_type: str = db.Column(db.ARRAY(db.String))
    due_diligence_level: str = db.Column(db.ARRAY(db.String))
    entity_type: str = db.Column(db.ARRAY(db.String))
    role: str = db.Column(db.ARRAY(db.String))
    policy_quote: str = db.Column(db.Text)
    internal_evidence_source: list = db.Column(db.ARRAY(db.String))
    external_evidence_source: list = db.Column(db.ARRAY(db.String))
    client_evidence_source: list = db.Column(db.ARRAY(db.String))
    data_point: str = db.Column(db.String(255))
    action_description: str = db.Column(db.Text)
    __table_args__ = (
        db.PrimaryKeyConstraint(
            kyc_id, data_point,
        ),
    )

@dataclass
class KycOps(db.Model):
    ops_id: int = db.Column(db.Integer, primary_key=True)
    ops_name: str = db.Column(db.String(255), nullable=False)
    ops_designation: str = db.Column(db.String(255), nullable=False)

@dataclass
class Policy(db.Model):
    policy_id: int = db.Column(db.Integer, primary_key=True)
    policy_name: str = db.Column(db.String(255), nullable=False)
    policy_version: str = db.Column(db.String(50), nullable=False)
    policy_file_path: str = db.Column(db.String(255), nullable=False)
