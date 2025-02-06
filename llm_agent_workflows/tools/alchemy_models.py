from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, ARRAY
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Table: client
class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)
    client_info_file_path = Column(String(255), nullable=False)

# Table: kyc_ops
class KycOps(Base):
    __tablename__ = "kyc_ops"
    ops_id = Column(Integer, primary_key=True, autoincrement=True)
    ops_name = Column(String(255), nullable=False)
    ops_designation = Column(String(255), nullable=False)

class Policy(Base):
    __tablename__ = "policy"
    
    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_name = Column(String(255), nullable=False)
    policy_version = Column(String(50), nullable=False)
    policy_file_path = Column(String(255), nullable=False)
    processed_policy_json = Column(Text)

# Table: kyc_process
class KycProcess(Base):
    __tablename__ = "kyc_process"
    kyc_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.client_id", ondelete="CASCADE"), nullable=False)
    ops_id = Column(Integer, ForeignKey("kyc_ops.ops_id", ondelete="CASCADE"), nullable=False)
    initiation_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    overall_status = Column(String(50), nullable=False)
    policy_id = Column(Integer, ForeignKey("policy.policy_id", ondelete="CASCADE"), nullable=False)
    risk_assessment_summary = Column(Text)
    risk_tier = Column(String(100))

    client = relationship("Client", backref="kyc_processes")
    ops = relationship("KycOps", backref="kyc_processes")

# Table: actions (Composite Primary Key)
class Actions(Base):
    __tablename__ = "actions"

    # Composite Primary Key
    kyc_id = Column(Integer, ForeignKey("kyc_process.kyc_id", ondelete="CASCADE"), primary_key=True)
    data_point = Column(String(255), primary_key=True)

    # Other columns
    latest_action_activity = Column(String(50), nullable=False)
    business_type = Column(ARRAY(Text))
    due_diligence_level = Column(ARRAY(Text))
    entity_type = Column(ARRAY(Text))
    role = Column(ARRAY(Text))
    policy_quote = Column(Text)
    internal_evidence_source = Column(ARRAY(Text))
    external_evidence_source = Column(ARRAY(Text))
    client_evidence_source = Column(ARRAY(Text))
    action_description = Column(Text)
    client_evidence_file_path = Column(Text)
    client_evidence_summary = Column(Text)

# Table: action_data_point
class ActionDataPoint(Base):
    __tablename__ = "action_data_point"
    action_id = Column(Integer, primary_key=True)
    action_description = Column(Text, nullable=False)
    data_point_description = Column(Text, nullable=False)
    internal_evidence = Column(Text, nullable=False)
    public_evidence = Column(Text, nullable=False)
    client_evidence = Column(Text, nullable=False)

# Table: policy_action_data_point (Join Table between policy & actions)
class PolicyActionDataPoint(Base):
    __tablename__ = "policy_action_data_point"
    policy_id = Column(Integer, ForeignKey("policy.policy_id", ondelete="CASCADE"), primary_key=True)
    action_id = Column(Integer, ForeignKey("action_data_point.action_id", ondelete="CASCADE"), primary_key=True)