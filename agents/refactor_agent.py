from core.llm import get_llm

llm = get_llm()

def refactor_code(code):

    prompt = f"""
You are a senior software engineer.

Refactor the following code to improve:

- readability
- structure
- maintainability
- performance

Keep functionality the same.

Code:
{code}

Return only improved code.
"""

    improved = llm.invoke(prompt)

    improved = str(improved)

    improved = improved.replace("```python", "")
    improved = improved.replace("```", "")

    return improved.strip()