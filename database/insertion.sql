INSERT INTO client (client_name, client_info_file_path) VALUES 
('AFC Bournemouth Limited', '/path/to/client/file'),
('The Arsenal Football Club Ltd', '/path/to/client/file'),
('Aston Villa FC Limited', '/path/to/client/file'),
('Brentford FC Limited', '/path/to/client/file'),
('Brighton & Hove Albion FC Ltd', '/path/to/client/file'),
('Burnley Football & Athletic Company Limited', '/path/to/client/file'),
('(THE) Chelsea Football Club Limited', '/path/to/client/file'),
('CPFC Limited', '/path/to/client/file'),
('Everton Football Club Company Limited', '/path/to/client/file'),
('Fulham Football Club Limited', '/path/to/client/file'),
('The Liverpool Football Club & Athletic Grounds Limited', '/path/to/client/file'),
('Luton Town Football Club 2020 Ltd', '/path/to/client/file'),
('Manchester City Football Club Limited', '/path/to/client/file'),
('Manchester United Football Club Limited', '/path/to/client/file'),
('Newcastle United Limited', '/path/to/client/file'),
('Nottingham Forest Football Club Limited', '/path/to/client/file'),
('Sheffield United Football Club Limited', '/path/to/client/file');

INSERT INTO kyc_ops (ops_name, ops_designation) VALUES
('John Smith', 'Associate'),
('Emma Johnson', 'VP'),
('Michael Brown', 'AVP'),
('Sophia Wilson', 'Senior Associate'),
('Liam Davis', 'Manager'),
('Olivia Martinez', 'Director'),
('Noah Taylor', 'Senior VP'),
('Ava Anderson', 'Analyst'),
('William Thomas', 'Lead Associate'),
('Emily Jackson', 'AVP'),
('James White', 'VP'),
('Isabella Harris', 'Associate'),
('Benjamin Clark', 'Manager'),
('Mia Lewis', 'Senior Associate'),
('Ethan Walker', 'Associate'),
('Charlotte Hall', 'Director'),
('Alexander Allen', 'Senior VP'),
('Amelia Young', 'Manager'),
('Daniel Scott', 'Lead Associate'),
('Harper King', 'Analyst');

INSERT INTO policy (policy_name, policy_version, policy_file_path) VALUES 
('JMLSG Part One June 2020 (amended July 2022)', 'v1', '/some/path.pdf'),
('JMLSG Part Two June 2020 (amended July 2022)', 'v2', '/some/path2.pdf');

INSERT INTO kyc_process (client_id, ops_id, policy_id, initiation_timestamp, overall_status) VALUES
(2, 2, 1, '2024-02-05 10:30:00', 'In Progress'),
(2, 3, 1, '2024-02-04 15:45:00', 'Completed'),
(4, 5, 1, '2024-02-02 14:10:00', 'In Progress'),
(5, 4, 1, '2024-02-01 08:05:00', 'Completed');

