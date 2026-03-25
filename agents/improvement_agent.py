from core.llm import get_llm

llm = get_llm()

def improve_code(code, feedback):

    prompt = f"""
You are a senior software engineer.

Improve the following code based on feedback.

Feedback:
{feedback}

Code:
{code}

Return improved code only.
"""

    improved = llm.invoke(prompt)

    improved = str(improved)

    improved = improved.replace("```python", "")
    improved = improved.replace("```", "")

    return {
    "improved_code": improved
    }