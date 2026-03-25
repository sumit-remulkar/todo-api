from core.logger import log
from core.llm import get_llm

llm = get_llm()

def create_plan(prompt):
    log("📐 Planner generating architecture")
    plan_prompt = f"""
You are a senior Python backend engineer.

Design the file structure for a FastAPI backend project.

Return ONLY file paths.

Example:

backend/main.py
backend/models.py
backend/routes.py
backend/database.py
requirements.txt

Project:
{prompt}
"""

    plan = llm.invoke(plan_prompt)

    return {
    "architecture": architecture
    }