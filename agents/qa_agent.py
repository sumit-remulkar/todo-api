from core.llm import get_llm

llm = get_llm()


def generate_tests(project_spec):

    prompt = f"""
You are a QA engineer.

Write pytest tests for the project.

Specification:
{project_spec}
"""

    tests = llm.invoke(prompt)

    return str(tests)