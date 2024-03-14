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
    """
    Provides authentication functionality for the admin panel.

    Methods:
    - verify_password: Verifies if the entered password matches the hashed password.
    - authenticate_admin: Authenticates the admin using the provided username and password.
    - generate_token: Generates a JWT token for the authenticated admin.
    - login: Logs in the admin by authenticating the provided credentials and generating a token.
    - logout: Logs out the admin by clearing the session.
    - authenticate: Authenticates the admin based on the token stored in the session.
    """

    async def verify_password(self, entered_password: str, hashed_password: str):
        """
        Verifies if the entered password matches the hashed password.

        Args:
        - entered_password: The password entered by the admin.
        - hashed_password: The hashed password stored in the database.

        Returns:
        - True if the entered password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(entered_password, hashed_password)

    async def authenticate_admin(self, username: str, password: str):
        """
        Authenticates the admin using the provided username and password.

        Args:
        - username: The username entered by the admin.
        - password: The password entered by the admin.

        Returns:
        - True if the admin is authenticated, False otherwise.
        """
        if username == config.admin_panel.admin_username:
            if await self.verify_password(password, hashed_password):
                return True
        return False

    def generate_token(self):
        """
        Generates a JWT token for the authenticated admin.

        Returns:
        - The generated JWT token.
        """
        expire = datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
        payload = {
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, config.admin_panel.secret_key, algorithm="HS256")

    async def login(self, request: Request) -> bool:
        """
        Logs in the admin by authenticating the provided credentials and generating a token.

        Args:
        - request: The HTTP request object.

        Returns:
        - True if the admin is successfully logged in, False otherwise.
        """
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
            """
            Authenticates the request using the provided token.

            Args:
                request (Request): The request object containing the session token.

            Returns:
                bool: True if the token is valid and not expired, False otherwise.
            """
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

