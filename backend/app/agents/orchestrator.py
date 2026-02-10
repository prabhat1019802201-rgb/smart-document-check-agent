from langgraph.graph import StateGraph

from app.agents.state import ValidationState
from app.agents.extraction_node import extraction_node
from app.agents.update_documents_node import update_documents_node
from app.agents.validation_node import validation_node
from app.agents.cross_validation_node import cross_validation_node
from app.agents.explanation_node import explanation_node


def build_validation_graph():
    """
    Builds the end-to-end validation graph.

    Flow:
    Upload
      ↓
    Extraction (PyPDF / OCR later)
      ↓
    Update documents_by_type (case memory)
      ↓
    Document-level validation
      ↓
    Cross-document validation
      ↓
    GenAI explanation
    """

    graph = StateGraph(ValidationState)

    # ----------------------------
    # Register nodes
    # ----------------------------
    graph.add_node("extract", extraction_node)
    graph.add_node("update_documents", update_documents_node)
    graph.add_node("validate", validation_node)
    graph.add_node("cross_validate", cross_validation_node)
    graph.add_node("explain", explanation_node)

    # ----------------------------
    # Define execution order
    # ----------------------------
    graph.set_entry_point("extract")

    graph.add_edge("extract", "update_documents")
    graph.add_edge("update_documents", "validate")
    graph.add_edge("validate", "cross_validate")
    graph.add_edge("cross_validate", "explain")

    graph.set_finish_point("explain")

    return graph.compile()
