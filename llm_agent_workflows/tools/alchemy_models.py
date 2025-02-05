from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, ARRAY
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Table: client
class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)

# Table: kyc_ops
class KycOps(Base):
    __tablename__ = "kyc_ops"
    ops_id = Column(Integer, primary_key=True, autoincrement=True)
    ops_name = Column(String(255), nullable=False)
    ops_designation = Column(String(255), nullable=False)

# Table: policy
class Policy(Base):
    __tablename__ = "policy"
    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_name = Column(String(255), nullable=False)
    policy_version = Column(String(50), nullable=False)

# Table: kyc_process
class KycProcess(Base):
    __tablename__ = "kyc_process"
    kyc_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.client_id", ondelete="CASCADE"), nullable=False)
    ops_id = Column(Integer, ForeignKey("kyc_ops.ops_id", ondelete="CASCADE"), nullable=False)
    initiation_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    overall_status = Column(String(50), nullable=False)

    client = relationship("Client", backref="kyc_processes")
    ops = relationship("KycOps", backref="kyc_processes")

# Table: actions (Composite Primary Key)
class Actions(Base):
    __tablename__ = "actions"
    
    kyc_id = Column(Integer, ForeignKey("kyc_process.kyc_id", ondelete="CASCADE"), primary_key=True)
    data_point = Column(String(255), primary_key=True)
    latest_action_activity = Column(String(50), nullable=False)
    business_type = Column(String(255))
    due_diligence_level = Column(String(255))
    entity_type = Column(String(255))
    role = Column(String(255))
    policy_quote = Column(Text)
    internal_evidence_source = Column(ARRAY(Text))
    external_evidence_source = Column(ARRAY(Text))
    client_evidence_source = Column(ARRAY(Text))
    action_description = Column(Text)
    policy_id = Column(Integer, ForeignKey("policy.policy_id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    kyc_process = relationship("KycProcess", backref="actions")
    policy = relationship("Policy", backref="actions")

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