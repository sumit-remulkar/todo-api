from core.llm import get_llm

llm = get_llm()

def select_stack(prompt):

    stack_prompt = f"""
    You are a senior software architect.

    Choose a tech stack for this project.

    IMPORTANT RULES:
    - Backend MUST use Python FastAPI
    - Do NOT suggest Node.js
    - Use Python ecosystem tools
    - Database can be SQLite or PostgreSQL
    - Frontend can be React (optional)

    Project:
    {prompt}

    Return stack in simple format.
    """

    result = llm.invoke(stack_prompt)

    return result


def choose(prompt):
    return select_stack(prompt)