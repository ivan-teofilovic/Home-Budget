from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.expense.models import Expense


class CategoryName(str, Enum):
    FOOD = "FOOD"
    TAXI = "TAXI"
    RENT = "RENT"
    HOBBIES = "HOBBIES"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"


class CategoryBase(SQLModel):
    name: CategoryName = Field(index=True)


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)

    expenses: list["Expense"] = Relationship(back_populates="category")


class CategoryPublic(CategoryBase):
    id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass
