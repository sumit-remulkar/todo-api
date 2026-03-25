from langgraph.graph import StateGraph, END

from agents.product_manager_agent import create_product_spec
from agents.planner_agent import create_plan
from agents.coder_agent import generate_code
from agents.qa_agent import generate_tests
from agents.devops_agent import generate_docker_setup


class AgentState(dict):
    prompt: str
    spec: str
    plan: str
    code: str


def product_manager(state):
    spec = create_product_spec(state["prompt"])
    state["spec"] = spec
    return state


def planner(state):
    plan = create_plan(state["spec"])
    state["plan"] = plan
    return state


def coder(state):
    code = generate_code(state["plan"], state["prompt"])
    state["code"] = code
    return state


def tester(state):
    generate_tests(state["prompt"])
    return state


def deploy(state):
    generate_docker_setup(state["prompt"])
    return state


graph = StateGraph(AgentState)

graph.add_node("product_manager", product_manager)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("tester", tester)
graph.add_node("deploy", deploy)

graph.set_entry_point("product_manager")
graph.add_edge("coder", "reviewer")
graph.add_edge("reviewer", "improver")
graph.add_edge("product_manager", "planner")
graph.add_edge("planner", "coder")
graph.add_edge("coder", "tester")
graph.add_edge("tester", "deploy")
graph.add_edge("deploy", END)

agent_graph = graph.compile()