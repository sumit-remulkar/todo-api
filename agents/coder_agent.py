import code
import os
from core.memory import get_files
from core.llm import get_llm
from core.logger import log

llm = get_llm()


def generate_code(file_path, project_prompt):
    log(f"👨‍💻 Generating code for {file_path}")

    existing_files = get_files()

    prompt = f"""
You are a senior full-stack developer.

Project description:
{project_prompt}

Existing project files:
{existing_files}

Generate code for file:
{file_path}

Return only code.
"""

    result = llm.invoke(prompt)

    if hasattr(result, "content"):
        code = result.content
    else:
        code = result

    code = str(code)

    code = code.replace("```python", "")
    code = code.replace("```javascript", "")
    code = code.replace("```jsx", "")
    code = code.replace("```", "")

    return code.strip()


def generate(structure):

    files = [
        "backend/main.py",
        "backend/models.py",
        "backend/routes.py",
        "backend/database.py"
    ]

    for file in files:

        code = generate_code(file, structure)

        save_file(
            f"workspace/generated_projects/generated_project/{file}",
            code
        )

    return {"files_created": files}


def save_file(path, content):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)

    return {
    "code": code
    }