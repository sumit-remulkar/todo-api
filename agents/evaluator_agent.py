from core.llm import get_llm

llm = get_llm()

def evaluate_code(output):

    prompt = f"""
Analyze the following program output.

Output:
{output}

Is the program working correctly?

Return:
GOOD
or
IMPROVE
"""

    result = llm.invoke(prompt)

    return str(result).strip()