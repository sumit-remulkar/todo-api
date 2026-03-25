from langgraph.graph import StateGraph, END
from core.agent_graph import agent_graph
from agents import (
    planner_agent,
    coder_agent,
    debugger_agent,
    test_agent,
    devops_agent
)
from agents.product_manager_agent import create_product_spec as product_manager
from agents.run_agent import run_project
from typing import TypedDict
from agents.reviewer_agent import review_code
from agents.improvement_agent import improve_code


class AgentState(TypedDict):
    prompt: str
    plan: str
    code: str
    tests: bool
    error: str


def planner(state: AgentState):
    plan = planner_agent.create_plan(state["prompt"])
    state["plan"] = plan
    return state


def coder(state):
    code = coder_agent.generate(state["plan"])
    state["code"] = code
    return state


def reviewer(state):

    review = review_code(state)

    state.get("review", "") = review

    return state


def improver(state):

    code = state.get("code", "")
    review = state.get("review", "")

    improved = improve_code(code, review)

    state["code"] = improved

    return state


def tester(state):
    result = test_agent.run(state)
    state["tests"] = result
    return state


def debugger(state):
    fix = debugger_agent.fix(state.get("error"))
    state["fix"] = fix
    return state


def devops(state):
    result = devops_agent.generate(state)
    state["deploy"] = result
    return state


graph = StateGraph(AgentState)

# nodes
graph.add_node("product_manager", product_manager)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)
graph.add_node("improver", improver)
graph.add_node("tester", tester)
graph.add_node("debugger", debugger)
graph.add_node("deploy", devops)

graph.set_entry_point("product_manager")

# edges
graph.add_edge("product_manager", "planner")
graph.add_edge("planner", "coder")
graph.add_edge("coder", "reviewer")
graph.add_edge("reviewer", "improver")
graph.add_edge("improver", "tester")


def check_tests(state):
    if state["tests"]:
        return "deploy"
    return "debugger"


graph.add_conditional_edges(
    "tester",
    check_tests,
    {
        "deploy": "deploy",
        "debugger": "debugger"
    }
)

graph.add_edge("debugger", "coder")
graph.add_edge("deploy", END)

agent_graph = graph.compile()

def run_agent(prompt):

    state = {
    "prompt": prompt,

    "plan": "",
    "architecture": "",

    "code": "",
    "review": "",
    "improved_code": "",

    "tests": "",
    "result": ""
    }

    print("Starting AI Software Engineer Agent...\n")

    result = agent_graph.invoke(state)

    print("\nAgent run completed.")

    return result