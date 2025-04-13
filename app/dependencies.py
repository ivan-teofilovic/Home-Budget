from typing import Annotated

from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session

from app.auth.models import User
from app.auth.service import verify_access_token, get_user
from app.database import engine
from app.exceptions import unauthorized_exception


class HashService:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]

HashDep = Annotated[HashService, Depends()]


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    payload = await verify_access_token(token)

    if not payload:
        raise unauthorized_exception

    username = payload.get("sub")

    if not username:
        raise unauthorized_exception

    user = await get_user(username, session)

    if not user:
        raise unauthorized_exception
    return user
