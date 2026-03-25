from typing import TypedDict


class AgentState(TypedDict):

    prompt: str

    plan: str
    architecture: str

    code: str
    review: str
    improved_code: str

    tests: str
    result: str