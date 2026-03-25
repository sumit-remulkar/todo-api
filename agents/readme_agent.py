from core.llm import get_llm

llm = get_llm()

def generate_readme(project_prompt):

    prompt = f"""
You are a senior software engineer.

Generate a professional README.md for the following project.

Project idea:
{project_prompt}

Include sections:

- Project Title
- Description
- Installation
- Usage
- Project Structure
- Example
- License

Return markdown format.
"""

    readme = llm.invoke(prompt)

    return readme