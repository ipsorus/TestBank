from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_id(db: Session, credit_id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=credit_id).first()

    # @staticmethod
    # def delete_account(db: Session, account_id: int) -> None:
    #     account = db.query(Account).filter_by(id=account_id).first()
    #
    #     if account:
    #         db.delete(account)
    #         db.commit()