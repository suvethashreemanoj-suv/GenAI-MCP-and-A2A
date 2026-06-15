import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://apiv5.hareeshworks.in/v1")
MODEL_ID = os.getenv("MODEL_ID", "deepseek-chat")

ML_AGENT_HOST = os.getenv("ML_AGENT_HOST", "127.0.0.1")
ML_AGENT_PORT = int(os.getenv("ML_AGENT_PORT", "8004"))

NLP_AGENT_URL = os.getenv("NLP_AGENT_URL", "http://172.16.32.51:8005")
CV_AGENT_URL = os.getenv("CV_AGENT_URL", "http://localhost:8006")
