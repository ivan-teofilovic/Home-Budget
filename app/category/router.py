from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from typing import List

from app.dependencies import get_current_user, SessionDep
from app.category.models import CategoryCreate, CategoryUpdate, CategoryPublic
from app.category.service import create, read_all, delete, update

router = APIRouter(dependencies=[Depends(get_current_user)], tags=["category"])


@router.get("/categories", response_model=List[CategoryPublic])
async def get_categories(session: SessionDep):
    return await read_all(session)


@router.post("/category", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, session: SessionDep):
    return await create(category, session)


@router.delete("/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, session: SessionDep):
    await delete(category_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/category/{category_id}", response_model=CategoryPublic)
async def update_category(
    category_id: int, category: CategoryUpdate, session: SessionDep
):
    return await update(category_id, category, session)
