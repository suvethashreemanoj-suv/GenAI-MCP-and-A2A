import os
from dotenv import load_dotenv

load_dotenv(override=True)


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")


LLM_API_KEY = _strip_quotes(
    os.getenv("OPENROUTER_API_KEY") or os.getenv("DEEPSEEK_API_KEY", "")
)
LLM_BASE_URL = _strip_quotes(
    os.getenv("OPENROUTER_BASE_URL")
    or os.getenv("DEEPSEEK_BASE_URL", "https://openrouter.ai/api/v1")
)
MODEL_ID = _strip_quotes(os.getenv("MODEL_ID", "meta-llama/llama-4-scout"))

# Backward-compatible aliases used across the codebase
OPENROUTER_API_KEY = LLM_API_KEY
OPENROUTER_BASE_URL = LLM_BASE_URL

OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8003")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "CV-Research-Agent")

CV_AGENT_HOST = os.getenv("CV_AGENT_HOST", "0.0.0.0")
CV_AGENT_PUBLIC_HOST = os.getenv("CV_AGENT_PUBLIC_HOST", "127.0.0.1")
CV_AGENT_PORT = int(os.getenv("CV_AGENT_PORT", "8003"))
CV_AGENT_PUBLIC_URL = _strip_quotes(os.getenv("CV_AGENT_PUBLIC_URL", "")).rstrip("/")


def get_public_base_url() -> str:
    """Public URL teammates use (tunnel URL or LAN IP)."""
    if CV_AGENT_PUBLIC_URL:
        return CV_AGENT_PUBLIC_URL
    return f"http://{CV_AGENT_PUBLIC_HOST}:{CV_AGENT_PORT}"

ML_AGENT_URL = os.getenv("ML_AGENT_URL", "http://127.0.0.1:8002")
NLP_AGENT_URL = os.getenv("NLP_AGENT_URL", "http://127.0.0.1:8005")
