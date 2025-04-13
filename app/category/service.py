from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.category.models import Category, CategoryCreate, CategoryUpdate


async def create(category: CategoryCreate, session: Session) -> Category:
    existing_category = await read_by_name(category.name, session)
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(**category.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


async def read_all(session: Session) -> List[Category]:
    return session.exec(select(Category)).all()


async def read_by_id(category_id: int, session: Session) -> Category:
    return session.exec(select(Category).where(Category.id == category_id)).first()


async def read_by_name(category_name: str, session: Session) -> Category:
    return session.exec(select(Category).where(Category.name == category_name)).first()


async def update(
    category_id: int, category_update: CategoryUpdate, session: Session
) -> Category:
    category = await read_by_id(category_id, session)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    category.name = category_update.name
    session.commit()
    session.refresh(category)
    return category


async def delete(category_id: int, session: Session):
    category = await read_by_id(category_id, session)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    session.delete(category)
    session.commit()
