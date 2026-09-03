from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String

from src.main.api.db.base import Base

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    credit_id = Column(Integer, ForeignKey('credit.id'), nullable=False)
    to_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    from_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f'<Transaction(id={self.id}, credit_id={self.credit_id}, '
                f'to_account_id={self.to_account_id}, from_account_id={self.from_account_id}, '
                f'amount={self.amount}, transaction_type={self.transaction_type}, '
                f'created_at={self.created_at})>')