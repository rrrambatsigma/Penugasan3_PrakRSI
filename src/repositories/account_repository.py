from sqlmodel import Session, select
from src.database.schema import Account

def create_account(db: Session, account: Account):
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account_by_id(db: Session, account_id: int):
    return db.get(Account, account_id)

def get_all_accounts(db: Session):
    return db.exec(select(Account)).all()

def delete_account(db: Session, account: Account):
    db.delete(account)
    db.commit()