from smolagents import CodeAgent, InferenceClientModel

from config import HF_TOKEN, MAX_AGENT_STEPS, MODEL_ID, PROMPTS_DIR
from tools import save_report, search_tool


def _load_system_prompt() -> str:
    return (PROMPTS_DIR / "system_prompt.md").read_text(encoding="utf-8")


def build_agent() -> CodeAgent:
    """Constructs the Startup Validation Agent: a smolagents CodeAgent wired up
    with web search and report-saving tools, guided by the validation workflow
    prompt.
    """
    model = InferenceClientModel(model_id=MODEL_ID, token=HF_TOKEN)
    agent = CodeAgent(
        tools=[search_tool, save_report],
        model=model,
        max_steps=MAX_AGENT_STEPS,
        add_base_tools=False,
    )
    agent.prompt_templates["system_prompt"] += "\n\n" + _load_system_prompt()
    return agent


def run_validation(startup_idea: str) -> str:
    """Runs the full validation workflow for a raw startup idea and returns the
    agent's final answer (executive summary + saved report path).
    """
    agent = build_agent()
    task = (
        "Validate the following startup idea and produce the full investor-style "
        f"report as instructed in your system prompt:\n\n{startup_idea}"
    )
    return agent.run(task)


if __name__ == "__main__":
    import sys

    idea = " ".join(sys.argv[1:]) or input("Describe your startup idea: ")
    result = run_validation(idea)
    print("\n=== RESULT ===\n")
    print(result)
