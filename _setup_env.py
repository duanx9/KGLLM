import os
from src.config_logger import logger
from dotenv import load_dotenv

def load_local_env(env: str):
    os.environ["GIT_PYTHON_REFRESH"] = "quiet" # delete warning from pipeline execution