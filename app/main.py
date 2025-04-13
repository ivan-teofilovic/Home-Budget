from fastapi import FastAPI

from app.expense.router import router as expense_router
from app.category.router import router as category_router
from app.auth.router import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(expense_router)
