from app.services.validation_persistence import persist_validation_results


def persistence_node(state, db):
    persist_validation_results(
        db=db,
        document_id=state["document_id"],
        status=state["validation_status"],
        severity=state["severity"],
        ocr_confidence=state["ocr_confidence"],
        issues=state["issues"]
    )

    return state
