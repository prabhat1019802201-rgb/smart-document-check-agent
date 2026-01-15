from langchain_community.llms import Ollama
from app.agents.prompts import EXPLANATION_PROMPT
from app.services.historical_memory_reader import fetch_historical_context


llm = Ollama(
    model="qwen2.5:3b",
    #base_url="http://192.168.1.22:11434",
    temperature=0.0
)

def explanation_node(state):
    issues = state.get("issues", [])
    db = state.get("db")
    document_type = state.get("document_type")

    if not issues:
        return state

    # -------------------------------------------------
    # Unsupported document → static explanation
    # -------------------------------------------------
    if issues[0].get("issue_type") == "Unsupported":
        state["genai_explanation"] = (
            "Automated validation is not available for this document type. "
            "Please route this document for manual review."
        )
        return state

    # -------------------------------------------------
    # Build enriched context using historical memory
    # -------------------------------------------------
    enriched_issue_descriptions = []

    for issue in issues:
        historical_context = None

        if db:
            historical_context = fetch_historical_context(
                db=db,
                document_type=document_type,
                issue_type=issue["issue_type"],
                field_name=issue["field_name"]
            )

        description = (
            f"Issue Type: {issue['issue_type']}, "
            f"Field: {issue['field_name']}, "
            f"Severity: {issue['severity']}"
        )

        if historical_context:
            description += (
                f"\nHistorical Insight: This issue has been observed before. "
                f"Common resolution(s): {', '.join(historical_context)}"
            )

        enriched_issue_descriptions.append(description)

    prompt = EXPLANATION_PROMPT.format(
        document_type=document_type,
        issues="\n\n".join(enriched_issue_descriptions)
    )

    # -------------------------------------------------
    # Call LLM safely
    # -------------------------------------------------
    try:
        response = llm.invoke(prompt)
        state["genai_explanation"] = response
    except Exception as e:
        print("WARNING | GenAI unavailable:", str(e))
        state["genai_explanation"] = (
            "Issues were identified using predefined validation rules. "
            "Historical resolution data was considered where available."
        )

    return state
