from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import GraphState
from graph.nodes import (
    retrieve_docs,
    generate_answer
)

workflow = StateGraph(
    GraphState
)

workflow.add_node(
    "retrieve",
    retrieve_docs
)

workflow.add_node(
    "generate",
    generate_answer
)

workflow.add_edge(
    START,
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "generate"
)

workflow.add_edge(
    "generate",
    END
)

graph = workflow.compile()