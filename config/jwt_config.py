from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class JWTConfig(BaseSettings):
    JWT_SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE_TIME: str


jwt_cfg = JWTConfig()
