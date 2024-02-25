from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from config import load_config, Config


config: Config = load_config(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(config.admin_panel.admin_password)


class AdminAuth(AuthenticationBackend):
    async def verify_password(self, entered_password: str, hashed_password: str):
        return pwd_context.verify(entered_password, hashed_password)

    async def authenticate_admin(self, username: str, password: str):
        if username == config.admin_panel.admin_username:
            if await self.verify_password(password, hashed_password):
                return True
        return False

    def generate_token(self):
        expire = datetime.utcnow() + timedelta(days=7)  # Token expires in 7 day
        payload = {
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, config.admin_panel.secret_key, algorithm="HS256")

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        is_auth = await self.authenticate_admin(username, password)

        if not is_auth:
            return False

        token = self.generate_token()
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            payload = jwt.decode(token, config.admin_panel.secret_key, algorithms=["HS256"])
            if payload:
                return True
        except jwt.ExpiredSignatureError:
            # Token has expired
            return False
        except jwt.InvalidTokenError:
            # Token is invalid for any other reason
            return False

