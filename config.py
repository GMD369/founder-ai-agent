import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = ROOT_DIR / "prompts"
TEMPLATES_DIR = ROOT_DIR / "templates"
REPORTS_DIR = ROOT_DIR / "reports"
DATA_DIR = ROOT_DIR / "data"

HF_TOKEN = os.getenv("HF_TOKEN", "")
MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")

MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "16"))

for _dir in (REPORTS_DIR, DATA_DIR):
    _dir.mkdir(exist_ok=True)
