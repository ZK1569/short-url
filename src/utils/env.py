import os

from dotenv import load_dotenv


class EnvVariableMeta(type):

    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class EnvVariable(metaclass=EnvVariableMeta):
    def __init__(self):
        load_dotenv()

        self.environnement = self._get_env("ENV", "development")
        self.version = self._get_env("VERSION", "0.0.0")
        self.short_url_prefix = self._get_env("SHORT_URL_PREFIX")

        self.db_user = self._get_env("DB_USER")
        self.db_host = self._get_env("DB_HOST")
        self.db_name = self._get_env("DB_NAME")
        self.db_password = self._get_env("DB_PASSWORD")
        self.db_port = self._get_env("DB_PORT")

    @staticmethod
    def _get_env(env_path: str, default: str = "") -> str:
        val = os.getenv(env_path)
        return val if val else default
