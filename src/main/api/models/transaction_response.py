from datetime import datetime
from enum import Enum
from typing import List, Optional

from src.main.api.models.base_model import BaseModel


class TransactionType(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"

class Transaction(BaseModel):
    transactionId: int
    type: TransactionType
    amount: float | int
    fromAccountId: Optional[int]
    toAccountId: int
    createdAt: datetime
    creditId: Optional[int]

class AccountTransactionResponse(BaseModel):
    id: int
    number: str
    balance: float | int
    transactions: List[Transaction] = []