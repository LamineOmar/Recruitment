from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list
    CV_FILE_MAX_SIZE: int
    SIZE_OF_POST_DESCRIPTION: float
    GEMINI_API_KEY:str


    class Config:
        env_file = "src/.env"

def get_settings():
    return Settings()