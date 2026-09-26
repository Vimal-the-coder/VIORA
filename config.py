import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Application
    APP_NAME = os.getenv("VIORA_NAME", "VIORA")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # AI
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Voice
    VOICE_NAME = os.getenv(
        "VOICE_NAME",
        "en-IN-NeerjaNeural"
    )