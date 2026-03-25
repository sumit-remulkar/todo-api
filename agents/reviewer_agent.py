from core.llm import llm

def review_code(state):

    code = state["code"]

    prompt = f"""
Review this code and suggest improvements.

Code:
{code}
"""

    review = llm.invoke(prompt)

    return {
        "review": review
    }