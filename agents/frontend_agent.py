from core.llm import get_llm

llm = get_llm()

def generate_frontend_structure(prompt):

    frontend_prompt = f"""
You are a senior React developer.

Generate a React frontend folder structure for:

{prompt}

Return only file paths.

Example format:

frontend/package.json
frontend/App.jsx
frontend/components/Navbar.jsx
frontend/components/PostList.jsx
"""

    result = llm.invoke(frontend_prompt)

    return result

def generate_frontend_code(file, prompt):

    code_prompt = f"""
You are a senior React developer.

Project: {prompt}

Generate React code for this file:

{file}

Return only code.
"""

    return llm.invoke(code_prompt)