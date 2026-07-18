# Startup Validation Agent

An AI agent (built on [smolagents](https://github.com/huggingface/smolagents)) that
researches a startup idea end-to-end — competitors, market size, customer pain
points, SWOT/PESTEL, pricing, MVP roadmap, and risks — and produces an
investor-style Markdown report.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

copy .env.example .env
# then edit .env and set GROQ_API_KEY (free at https://console.groq.com/keys)
```

The default model is `llama-3.3-70b-versatile`, served via Groq's free-tier API
(fast inference, rate-limited by requests/tokens per minute rather than a small
one-time monthly credit). If you hit rate limits, set `MODEL_ID` in `.env` to
another model available on Groq (e.g. `llama-3.1-8b-instant` for a lighter/faster
option).

## Run

Streamlit UI:

```bash
streamlit run app.py
```

CLI:

```bash
python agent.py "A mobile app that helps freelance designers auto-generate client contracts and invoices using AI."
```

Reports are saved to `reports/` as Markdown files.

## Project structure

```
app.py                Streamlit UI
agent.py              Builds the smolagents CodeAgent and runs the validation workflow
config.py             Env vars, model id, paths
tools/                Custom tools: web search, report saving
prompts/              System prompt defining the 10-step validation workflow
templates/             Report section layout reference
reports/              Generated validation reports (gitignored)
data/                 Cache / scratch data (gitignored)
```

## Next steps

See the project report for the full functional module list (pricing engine,
revenue projection, business model canvas, go-to-market strategy, etc.) and
future enhancements (multi-agent architecture, RAG, financial forecasting,
pitch deck generation, dashboard analytics).
