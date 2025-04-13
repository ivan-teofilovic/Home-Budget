from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.category.models import Category
    from app.auth.models import User


class ExpenseBase(SQLModel):
    description: str = Field()
    amount: Decimal = Field(default=0, max_digits=5, decimal_places=3, index=True)
    category_id: int | None = Field(default=None, foreign_key="category.id", index=True)


class Expense(ExpenseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="usr.id", index=True)

    category: Optional["Category"] = Relationship(back_populates="expenses")
    user: Optional["User"] = Relationship(back_populates="expenses")


class ExpensePublic(ExpenseBase):
    id: int
    user_id: int


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    description: str | None
    amount: Decimal | None
    category_id: int | None
