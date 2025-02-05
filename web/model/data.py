from dataclasses import dataclass
from datetime import datetime

@dataclass
class Kyc:
    kycId: int
    clientId: int
    clientName: str
    date: datetime
    status: str
    afcStatus: str = 'none'
    riskRate: str = 'none'

@dataclass
class Client:
    clientId: int
    clientName: str
    # clientEmail: str

