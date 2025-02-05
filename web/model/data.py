from dataclasses import dataclass
from datetime import datetime

@dataclass
class Kyc:
    kycId: int
    clientId: int
    policyId:int
    clientName: str
    policyName: str
    triggerDate: datetime
    status: str
    afcStatus: str = 'none'
    riskRate: str = 'none'
