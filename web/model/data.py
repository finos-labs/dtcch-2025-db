from dataclasses import dataclass
from datetime import datetime

@dataclass
class Kyc:
    kyc_id: int
    client_id: int
    policy_id: int
    client_name: str
    policy_name: str
    trigger_date: datetime
    status: str
    afc_status: str = 'none'
    risk_rate: str = 'none'
