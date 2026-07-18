import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = ROOT_DIR / "prompts"
TEMPLATES_DIR = ROOT_DIR / "templates"
REPORTS_DIR = ROOT_DIR / "reports"
DATA_DIR = ROOT_DIR / "data"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_BASE = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1")
MODEL_ID = os.getenv("MODEL_ID", "llama-3.3-70b-versatile")

MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "10"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))

for _dir in (REPORTS_DIR, DATA_DIR):
    _dir.mkdir(exist_ok=True)
