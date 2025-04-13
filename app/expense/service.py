from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select, func

from app.auth.models import User
from app.category.models import Category
from app.expense.models import Expense, ExpenseUpdate
from app.expense.schemas import FilterParams


async def create(expense: Expense, user: User, session: Session) -> Expense:
    if expense.category_id:
        category = await read_by_id(expense.category_id, user, session)
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

    if user.balance < expense.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    user.balance -= expense.amount
    session.add(expense)
    session.add(user)
    session.commit()
    return expense


async def read_all(
    user: User, filter_query: FilterParams, session: Session
) -> List[Expense]:
    stmt = select(Expense).where(Expense.user_id == user.id)

    if filter_query.category_id is not None:
        stmt = stmt.where(Expense.category_id == filter_query.category_id)
    if filter_query.min_amount is not None:
        stmt = stmt.where(Expense.amount >= filter_query.min_amount)
    if filter_query.max_amount is not None:
        stmt = stmt.where(Expense.amount <= filter_query.max_amount)

    return session.exec(stmt).all()


async def read_by_id(expense_id: int, user: User, session: Session) -> Expense | None:
    return session.exec(
        select(Expense).where(Expense.name == expense_id, Expense.user_id == user.id)
    ).first()


async def update(
    expense_id: id, expense_update: ExpenseUpdate, user: User, session: Session
) -> Expense:
    expense = await read_by_id(expense_id, user, session)
    if not expense:
        raise HTTPException(status_code=400, detail="Expense does not exist")
    expense_data = expense_update.model_dump(exclude_unset=True)
    expense.sqlmodel_update(expense_data)
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


async def delete(expense_id: int, user: User, session: Session):
    expense = await read_by_id(expense_id, user, session)
    if not expense:
        raise HTTPException(status_code=400, detail="Expense does not exist")

    session.delete(expense)
    session.commit()


async def get_summary(user: User, session: Session):
    total_amount = session.exec(
        select(func.sum(Expense.amount)).where(Expense.user_id == user.id)
    ).one() or 0

    spending_per_category = session.exec(
        select(Category.name, func.sum(Expense.amount))
        .join(Category, Category.id == Expense.category_id)
        .where(Expense.user_id == user.id)
        .group_by(Category.name)
    ).all()

    return {
        "total_amount": total_amount,
        "spending_per_category": [
            {"category": name, "total": total} for name, total in spending_per_category
        ],
    }
