
def update_documents_node(state):
    """
    Accumulates extracted fields per document type at case level.
    """

    doc_type = state.get("document_type")
    extracted_fields = state.get("extracted_fields") or {}

    if not doc_type or not extracted_fields:
        return state

    documents = state.get("documents_by_type") or {}

    normalized_doc_type = doc_type.strip().lower()
    documents[normalized_doc_type] = extracted_fields

    state["documents_by_type"] = documents
    return state



