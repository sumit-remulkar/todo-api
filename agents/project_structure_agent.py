from core.llm import get_llm

llm = get_llm()

def generate_structure(prompt):

    structure_prompt = f"""
You are a senior full stack developer.

Create a project file structure for:

{prompt}

IMPORTANT RULES:
- Do NOT include explanations
- Do NOT include tree format
- Do NOT include /todo_app
- Only return file paths

Example format:

backend/main.py
backend/routes.py
backend/models.py
frontend/package.json
frontend/App.jsx
frontend/components/Navbar.jsx
frontend/components/PostList.jsx
database/schema.sql

Return ONLY the file paths.
"""

    return llm.invoke(structure_prompt)

def create_structure(stack):

    prompt = f"""
Generate project folder structure for the following stack:

{stack}

Return only folders and files.
"""

    result = llm.invoke(prompt)

    return result


def generate(stack):
    return create_structure(stack)