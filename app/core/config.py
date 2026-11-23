import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    RESET_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", "15"))
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DAILY_SEMANTIC_SEARCH_LIMIT: int = int(os.getenv("DAILY_SEMANTIC_SEARCH_LIMIT", "5"))

    @property
    def FRONTEND_URL(self) -> str:
        return self.ALLOWED_ORIGINS


settings = Settings()
