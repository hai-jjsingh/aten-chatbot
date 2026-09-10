from typing import TypedDict, List


class GraphState(TypedDict):
    question: str
    context: str
    sources: List[dict]
    answer: str