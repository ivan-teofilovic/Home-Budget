import jwt
from sqlmodel import Session, select

from app.auth.config import auth_settings
from app.auth.models import User


async def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.DecodeError:
        return None


async def get_user(username: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()


async def register_user(user: User, session: Session):
    session.add(user)
    session.commit()
