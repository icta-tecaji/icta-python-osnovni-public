from dataclasses import dataclass
from enum import Enum


class LoanStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass
class Loan:
    amount: float
    status: LoanStatus = LoanStatus.PENDING

    def reject(self):
        self.status = LoanStatus.REJECTED

    def rejected(self):
        return self.status == LoanStatus.REJECTED
