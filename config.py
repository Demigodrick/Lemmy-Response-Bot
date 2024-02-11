import os
from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    INSTANCE: str
    TRIGGER_1: str
    RESPONSES_1: str
    TRIGGER_2: str
    RESPONSES_2: str
    TRIGGER_3: str
    RESPONSES_3: str
    INCLUDE: str
    POLL_AMOUNT:int
    POLL_FREQ:int
    REACH:str
    CREATE_REPORT:bool

    class Config:
        env_file = ".env"
        
settings = Settings()