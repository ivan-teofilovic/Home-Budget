from decimal import Decimal
from typing import TYPE_CHECKING, List

from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.expense.models import Expense


class UserBase(SQLModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    __tablename__ = "usr"

    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    balance: Decimal = Field(default=1000.0)

    expenses: List["Expense"] = Relationship(back_populates="user")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
