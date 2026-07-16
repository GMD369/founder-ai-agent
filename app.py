from pathlib import Path

import streamlit as st

from agent import run_validation
from config import HF_TOKEN

st.set_page_config(page_title="Startup Validation Agent", page_icon="🚀", layout="wide")

st.title("🚀 Startup Validation Agent")
st.caption(
    "Describe your startup idea and get an AI-researched, investor-style "
    "validation report: competitors, market size, SWOT, pricing, MVP roadmap, and risks."
)

if not HF_TOKEN:
    st.warning(
        "No HF_TOKEN found. Copy `.env.example` to `.env` and add a free Hugging Face "
        "access token (from huggingface.co/settings/tokens) before running a validation."
    )

idea = st.text_area(
    "Describe your startup idea",
    height=140,
    placeholder=(
        "e.g. A mobile app that helps freelance designers automatically generate "
        "client contracts and invoices using AI."
    ),
)

run_clicked = st.button("Validate idea", type="primary", disabled=not HF_TOKEN)

if run_clicked:
    if not idea.strip():
        st.error("Please describe a startup idea first.")
    else:
        with st.spinner("Researching competitors, market, and risks... this can take a few minutes."):
            try:
                result = run_validation(idea)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Validation failed: {exc}")
            else:
                st.session_state["result"] = result

if "result" in st.session_state:
    st.markdown("## Result")
    st.markdown(st.session_state["result"])

    # If the agent's final answer references a saved report file, offer it for download.
    for line in str(st.session_state["result"]).splitlines():
        line = line.strip()
        if line.endswith(".md") and Path(line).exists():
            st.download_button(
                "Download full report (.md)",
                data=Path(line).read_text(encoding="utf-8"),
                file_name=Path(line).name,
                mime="text/markdown",
            )
            break
