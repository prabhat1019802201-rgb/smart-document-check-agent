

def update_documents_by_type(state):
    doc_type = (state.get("document_type") or "").lower()
    fields = state.get("extracted_fields", {})

    if not state.get("documents_by_type"):
        state["documents_by_type"] = {}

    if doc_type:
        state["documents_by_type"][doc_type] = fields

    return state

