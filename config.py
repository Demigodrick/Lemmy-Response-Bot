import os
from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    INSTANCE: str
    TRIGGER: str
    RESPONSES: str
    INCLUDE: str

    class Config:
        env_file = ".env"
        
settings = Settings()