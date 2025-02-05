-- Table: client
CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    client_info_file_path VARCHAR(255) NOT NULL
);

-- Table: kyc_ops
CREATE TABLE kyc_ops (
    ops_id SERIAL PRIMARY KEY,
    ops_name VARCHAR(255) NOT NULL,
    ops_designation VARCHAR(255) NOT NULL
);

-- Table: policy
CREATE TABLE policy (
    policy_id SERIAL PRIMARY KEY,
    policy_name VARCHAR(255) NOT NULL,
    policy_version VARCHAR(50) NOT NULL,
    policy_file_path VARCHAR(255) NOT NULL
);

-- Table: kyc_process
CREATE TABLE kyc_process (
    kyc_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    policy_id INT NOT NULL,
    ops_id INT NOT NULL,
    initiation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    overall_status VARCHAR(50) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE,
    FOREIGN KEY (policy_id) REFERENCES policy(policy_id) ON DELETE CASCADE,
    FOREIGN KEY (ops_id) REFERENCES kyc_ops(ops_id) ON DELETE CASCADE
);

-- Table: actions (Composite Primary Key)
CREATE TABLE actions (
    kyc_id INT NOT NULL,
    latest_action_activity VARCHAR(50) NOT NULL,
    business_type VARCHAR(255),
    due_diligence_level VARCHAR(255),
    entity_type VARCHAR(255),
    role VARCHAR(255),
    policy_quote TEXT,
    internal_evidence_source TEXT[],
    external_evidence_source TEXT[],
    client_evidence_source TEXT[],
    data_point VARCHAR(255),
    action_description TEXT,
    PRIMARY KEY (kyc_id, data_point),
    FOREIGN KEY (kyc_id) REFERENCES kyc_process(kyc_id) ON DELETE CASCADE
);
