from langgraph.graph import StateGraph
from app.agents.state import ValidationState
from app.agents.extraction_node import extraction_node
from app.agents.validation_node import validation_node
from app.agents.explanation_node import explanation_node

def build_validation_graph():
    graph = StateGraph(ValidationState)

    graph.add_node("extract", extraction_node)
    graph.add_node("validate", validation_node)
    graph.add_node("explain", explanation_node)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "validate")
    graph.add_edge("validate", "explain")
    graph.set_finish_point("explain")

    return graph.compile()
