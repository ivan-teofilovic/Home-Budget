from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from typing import List, Annotated

from app.dependencies import get_current_user, SessionDep
from app.expense.models import ExpenseCreate, ExpensePublic, Expense, ExpenseUpdate
from app.expense.schemas import FilterParams
from app.expense.service import create, read_all, get_summary, delete, update
from app.auth.models import User

router = APIRouter(dependencies=[Depends(get_current_user)], tags=["expense"])


@router.get("/expenses", response_model=List[ExpensePublic])
async def get_expenses(
    user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
    filter_query: FilterParams = Query(),
):
    return await read_all(user, filter_query, session)


@router.post("/expense", response_model=ExpensePublic, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
):
    return await create(Expense(**expense.model_dump(), user_id=user.id), user, session)


@router.get("/expense/summary")
async def get_expense_summary(
    user: Annotated[User, Depends(get_current_user)], session: SessionDep
):
    return await get_summary(user, session)


@router.delete("/expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
):
    return await delete(expense_id, user, session)


@router.patch("/expense/{expense_id}", response_model=ExpensePublic)
async def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
):
    return await update(expense_id, expense, user, session)
