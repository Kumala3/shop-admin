from dataclasses import dataclass
from typing import Optional

from sqlalchemy.engine.url import URL
from environs import Env


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS", subcast=int)
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    api_key : str, optional
        The API key used for authentication.
    shop_id : str, optional
        The ID of the shop.
    secretkey_1 : str, optional
        The secret key used for encryption.

    Methods
    -------
    from_env(env: Env) -> Miscellaneous:
        Creates the Miscellaneous object from environment variables.

    """

    api_key: str
    shop_id: str
    secretkey_1: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the Miscellaneous object from environment variables.

        Parameters
        ----------
        env : Env
            The environment object containing the required environment variables.

        Returns
        -------
        Miscellaneous
            The Miscellaneous object created from the environment variables.

        """
        api_key = env.str("API_KEY")
        shop_id = env.str("SHOP_ID")
        secretkey_1 = env.str("SECRETKEY_1")

        return Miscellaneous(api_key=api_key, shop_id=shop_id, secretkey_1=secretkey_1)


@dataclass
class AdminPanel:
    """
    Admin panel configuration class.

    This class holds settings for the admin panel.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    logo_url : str
        A string used to hold the URL of the logo.
    secret_key : str
        A string used to hold the secret key.
    """

    logo_url: str
    secret_key: str
    admin_username: str
    admin_password: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        logo_url = env.str("ADMIN_LOGO_URL")
        secret_key = env.str("ADMIN_SECRET_KEY")
        admin_username = env.str("ADMIN_USERNAME")
        admin_password = env.str("ADMIN_PASSWORD")

        return AdminPanel(
            logo_url=logo_url,
            secret_key=secret_key,
            admin_username=admin_username,
            admin_password=admin_password,
        )


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None
    admin_panel: Optional[AdminPanel] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        db=DbConfig.from_env(env),
        redis=RedisConfig.from_env(env),
        admin_panel=AdminPanel.from_env(env),
        misc=Miscellaneous.from_env(env),
    )
