-- Table: client
CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL
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
    policy_version VARCHAR(50) NOT NULL
);

-- Table: kyc_process
CREATE TABLE kyc_process (
    kyc_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    -- policy_id INT NOT NULL,
    ops_id INT NOT NULL,
    initiation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    overall_status VARCHAR(50) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE,
    -- FOREIGN KEY (policy_id) REFERENCES policy(policy_id) ON DELETE CASCADE,
    FOREIGN KEY (ops_id) REFERENCES kyc_ops(ops_id) ON DELETE CASCADE
);

-- Table: actions (Composite Primary Key)
CREATE TABLE actions (
    action_id INT NOT NULL,
    kyc_id INT NOT NULL,
    action_status VARCHAR(50) NOT NULL,
    latest_action_activity VARCHAR(50) NOT NULL,
    variable_1 VARCHAR(255), -- Adjust datatype as necessary
    variable_2 VARCHAR(255),
    variable_3 VARCHAR(255),
    variable_4 VARCHAR(255),
    variable_5 VARCHAR(255),
    variable_6 VARCHAR(255),
    policy_quote TEXT,
    reg_section VARCHAR(255),
    PRIMARY KEY (action_id, kyc_id),
    FOREIGN KEY (kyc_id) REFERENCES kyc_process(kyc_id) ON DELETE CASCADE
);

-- Table: action_data_point (Now only referencing action_id)
CREATE TABLE action_data_point (
    action_id INT PRIMARY KEY,
    action_description TEXT NOT NULL,
    data_point_description TEXT NOT NULL,
    internal_evidence TEXT NOT NULL,
    public_evidence TEXT NOT NULL,
    non_public_evidence TEXT NOT NULL
);

-- Table: policy_action_data_point (Join Table between policy & actions)
CREATE TABLE policy_action_data_point (
    policy_id INT NOT NULL,
    action_id INT NOT NULL,
    PRIMARY KEY (policy_id, action_id),
    FOREIGN KEY (policy_id) REFERENCES policy(policy_id) ON DELETE CASCADE,
    FOREIGN KEY (action_id) REFERENCES action_data_point(action_id) ON DELETE CASCADE
);

