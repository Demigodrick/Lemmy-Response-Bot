import os
from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    INSTANCE: str
    TRIGGER: str
    RESPONSES: str
    INCLUDE: str
    POLL_AMOUNT:int
    POLL_FREQ:int

    class Config:
        env_file = ".env"
        
settings = Settings()