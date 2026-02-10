from app.services.cross_document_rules import validate_cross_document_consistency


def cross_validation_node(state):
    """
    Runs cross-document consistency checks only when safe to do so.
    """

    documents = state.get("documents_by_type") or {}
    issues = state.get("issues") or []

    # Guard condition — VERY IMPORTANT
    if len(documents) < 2:
        state["issues"] = issues
        return state

    cross_issues = validate_cross_document_consistency(documents)

    # Tag issues clearly
    for issue in cross_issues:
        issue["source"] = "cross_document"

    issues.extend(cross_issues)
    state["issues"] = issues

    print("DEBUG | cross-doc running on:", list(documents.keys()))

    return state
