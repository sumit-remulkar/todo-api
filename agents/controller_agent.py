from core.llm import get_llm
from executor.run_project import run_backend
from agents.api_test_agent import test_api
from agents import coder_agent, debugger_agent, devops_agent, planner_agent, refactor_agent, stack_agent, test_agent
from executor.test_runner import run_tests

llm = get_llm()


def decide_next_action(prompt, state):

    controller_prompt = f"""
You are an AI software engineering manager.

Project goal:
{prompt}

Current project state:
{state}

Decide the next action.

Possible actions:

plan_project
generate_code
run_project
generate_tests
run_tests
debug_code
finish_project

Return only the action name.
"""

    action = llm.invoke(controller_prompt)

    return str(action).strip().lower()
def run_controller(prompt):

    state = {
        "planned": False,
        "code_generated": False,
        "backend_running": False,
        "tests_passed": False
    }

    while True:

        action = decide_next_action(prompt, state)

        print("\nAI Decision:", action)

        if action == "plan_project":

            print("Planning project...")
            state["planned"] = True

        elif action == "generate_code":

            print("Generating code...")
            state["code_generated"] = True

        elif action == "run_project":

            print("Starting backend server...")
            run_backend()
            state["backend_running"] = True

        elif action == "test_api":

            print("Generating tests...")
            tests = test_agent.generate()

            print("Running tests...")
            stdout, stderr = run_tests()

            print(stdout)

            if stderr:
                print("Tests failed:", stderr)
                state["tests_passed"] = False
            else:
                print("All tests passed")
                state["tests_passed"] = True

        elif action == "debug_code":

            print("Debugging project...")

        elif action == "finish_project":

            print("\nAI completed the project.")
            break