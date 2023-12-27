from pathlib import Path
from pydantic import BaseModel
from pydantic.v1 import BaseSettings

from dotenv import load_dotenv

import os

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "public.pem"
    algorithm: str = 'RS256'
    access_token_exp_minutes: int = 30


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
