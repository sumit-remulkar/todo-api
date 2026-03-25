from core.llm import get_llm
import subprocess
from core.logger import log

llm = get_llm()


def generate_tests(prompt):

    test_prompt = f"""
You are a senior QA engineer.

Write pytest tests for the following project:

{prompt}

Return Python test code only.
"""

    return llm.invoke(test_prompt)


def run(state):
    
    log("🧪 Running project tests")

    try:
        subprocess.run(
            ["pytest"],
            cwd="workspace/generated_projects/generated_project",
            check=True
        )

        state["tests"] = True
        return state

    except subprocess.CalledProcessError as e:

        state["tests"] = False
        state["error"] = str(e)

        return state
