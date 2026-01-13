from langgraph.graph import StateGraph
from app.agents.state import ValidationState
from app.agents.extraction_node import extraction_node
from app.agents.validation_node import validation_node


def build_validation_graph():
    graph = StateGraph(ValidationState)

    graph.add_node("extract", extraction_node)
    graph.add_node("validate", validation_node)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "validate")
    graph.set_finish_point("validate")

    return graph.compile()
