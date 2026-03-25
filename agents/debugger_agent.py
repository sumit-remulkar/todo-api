from core.llm import get_llm
from core.logger import log

llm = get_llm()

def fix(error):
    
    log("🐞 Debugging project error")

    prompt = f"""
You are a senior Python engineer.

Fix this error in the project.

ERROR:
{error}

Return only the corrected code or explanation.
"""

    response = llm.invoke(prompt)

    return response