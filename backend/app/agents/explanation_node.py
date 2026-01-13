from langchain_community.llms import Ollama
from app.agents.prompts import EXPLANATION_PROMPT


llm = Ollama(
    model="llama3.1:8b",
    temperature=0.0  # IMPORTANT: deterministic explanations
)


def explanation_node(state):
    issues = state.get("issues", [])

    # If no issues, nothing to explain
    if not issues:
        return state

    formatted_issues = "\n".join(
        f"- Issue Type: {i['issue_type']}, Field: {i['field_name']}, Severity: {i['severity']}"
        for i in issues
    )

    prompt = EXPLANATION_PROMPT.format(
        document_type=state.get("document_type"),
        issues=formatted_issues
    )

    response = llm.invoke(prompt)

    # Attach explanation to each issue (simple mapping)
    for issue in issues:
        issue["why_flagged"] = issue.get(
            "why_flagged",
            "Refer to explanation provided."
        )
        issue["suggested_action"] = issue.get(
            "suggested_action",
            "Refer to suggested corrective steps."
        )

    state["issues"] = issues
    state["genai_explanation"] = response

    return state
