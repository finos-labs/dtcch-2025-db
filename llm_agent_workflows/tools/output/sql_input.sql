Here is the SQL format for inserting a record into the `kyc_process` table and three related records into the `actions` table:

```sql
-- Insert a record into the kyc_process table
INSERT INTO kyc_process (
    kyc_id, status, risk_tier, risk_assessment_summary, client_id, created_at, updated_at
) VALUES (
    1, 'IN_PROGRESS', 'Medium', 'Initial risk assessment pending further review', 123, '2023-10-01 12:00:00', '2023-10-01 12:00:00'
);

-- Insert three related records into the actions table
INSERT INTO actions (
    kyc_id, data_point, latest_action_activity, business_type, due_diligence_level, entity_type, role, policy_quote, internal_evidence_source, external_evidence_source, client_evidence_source, action_description, uuid
) VALUES (
    1, 'Residential Address', 'PENDING', 'Other Business Type', 'Client Due Diligence', 'Private Individual', 'Organisation Senior Management', 'Identify the Natural Person Client Senior Manager\'s residential address', 'Client Data System', 'Credit Reference Agency', 'Utility Bill', 'Identify residential address', '123e4567-e89b-12d3-a456-426614174000'
), (
    1, 'Bank Account Verification', 'PENDING', 'Financial Services', 'Enhanced Due Diligence', 'Corporate Entity', 'Account Holder', 'Verify the bank account details of the corporate entity', 'Bank Records', 'Bank Verification Service', 'Bank Statement', 'Verify bank account details', '123e4567-e89b-12d3-a456-426614174001'
), (
    1, 'Identity Verification', 'PENDING', 'Retail', 'Simplified Due Diligence', 'Private Individual', 'Customer', 'Verify the identity of the customer', 'Customer Database', 'Government ID Verification Service', 'Passport', 'Verify customer identity', '123e4567-e89b-12d3-a456-426614174002'
);
```