from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.models import User
from app.core.auth import (
    SECRET_KEY,
    verify_password,
    create_access_token,
)
from app.deps import session


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        with session() as db:
            username, password = form["username"], form["password"]
            user = db.query(User).filter(User.login == username).first()
            if not user or not verify_password(
                password, user.hashed_password
            ):
                return False
        token = create_access_token(data={"sub": user.login})
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
