"""
Module to load environment variables from a .env file.
"""
import os
from dotenv import load_dotenv

class EnvironmentVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()  # Load .env once at initialization
        return cls._instance

    @staticmethod
    def get_max_words(default: int = None) -> int:
        return os.getenv("MAX_WORDS", default)

    @staticmethod
    def get_input_filename(default: str = None) -> list:
        return os.getenv("INPUT_FILENAME", default).split(',')

    @staticmethod
    def get_temperature(default: float = None) -> float:
        return float(os.getenv("TEMPERATURE", default))
