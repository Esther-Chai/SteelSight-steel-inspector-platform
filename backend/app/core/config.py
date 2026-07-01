# env vars
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str

    # Groq
    GROQ_API_KEY: str

    # Model
    MODEL_PATH: str = "weights/best.pt"

    class Config:
        env_file = ".env"

settings = Settings()