from pathlib import Path

import streamlit as st

from agent import run_validation
from config import HF_TOKEN, MODEL_ID

st.set_page_config(
    page_title="Startup Validation Agent",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    #MainMenu, header, footer { visibility: hidden; }

    html, body, [class*="css"] {
        font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 960px;
    }

    .app-header {
        border-bottom: 1px solid rgba(128, 128, 128, 0.25);
        padding-bottom: 1.25rem;
        margin-bottom: 2rem;
    }

    .app-header h1 {
        font-size: 1.9rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        margin-bottom: 0.35rem;
    }

    .app-header p {
        font-size: 0.98rem;
        opacity: 0.72;
        margin: 0;
    }

    .section-label {
        text-transform: uppercase;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        opacity: 0.55;
        margin-bottom: 0.5rem;
    }

    .stTextArea textarea {
        font-size: 0.95rem;
        border-radius: 6px;
    }

    div.stButton > button {
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
    }

    .report-card {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 8px;
        padding: 2rem 2.25rem;
        margin-top: 1.5rem;
    }

    .status-pill {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 0.15rem 0.65rem;
        border-radius: 999px;
        border: 1px solid rgba(128, 128, 128, 0.35);
        opacity: 0.85;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Configuration")
    st.markdown(f"**Model**  \n`{MODEL_ID}`")
    token_status = "Connected" if HF_TOKEN else "Not configured"
    st.markdown(f"**Hugging Face token**  \n{token_status}")
    st.divider()
    st.markdown(
        "This agent researches the market for a startup idea and produces a "
        "structured, investor-style validation report covering competitors, "
        "market size, SWOT, pricing, MVP roadmap, and risk."
    )
    st.divider()
    st.caption("Reports are also saved locally to the `reports/` folder.")

st.markdown(
    """
    <div class="app-header">
        <h1>Startup Validation Agent</h1>
        <p>Structured, research-backed validation for a startup idea — competitors,
        market sizing, SWOT, pricing, MVP roadmap, and risk assessment.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not HF_TOKEN:
    st.warning(
        "No Hugging Face token configured. Copy `.env.example` to `.env` and add a "
        "token from huggingface.co/settings/tokens before running a validation."
    )

st.markdown('<div class="section-label">Startup Idea</div>', unsafe_allow_html=True)
idea = st.text_area(
    label="Startup idea",
    label_visibility="collapsed",
    height=140,
    placeholder=(
        "e.g. A mobile app that helps freelance designers automatically generate "
        "client contracts and invoices using AI."
    ),
)

run_clicked = st.button("Validate Idea", type="primary", disabled=not HF_TOKEN)

if run_clicked:
    if not idea.strip():
        st.error("Please describe a startup idea first.")
    else:
        with st.spinner("Researching competitors, market, and risks — this can take a few minutes."):
            try:
                result = run_validation(idea)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Validation failed: {exc}")
            else:
                st.session_state["result"] = result

if "result" in st.session_state:
    st.markdown('<div class="section-label">Validation Report</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="report-card">{st.session_state["result"]}</div>',
        unsafe_allow_html=True,
    )

    for line in str(st.session_state["result"]).splitlines():
        line = line.strip()
        if line.endswith(".md") and Path(line).exists():
            st.download_button(
                "Download Full Report (.md)",
                data=Path(line).read_text(encoding="utf-8"),
                file_name=Path(line).name,
                mime="text/markdown",
            )
            break
