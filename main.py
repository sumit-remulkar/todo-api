from agents.debugger_agent import debug_code
from agents.planner_agent import create_plan
from agents.coder_agent import generate_code
from agents.readme_agent import generate_readme
from agents.stack_agent import select_stack
from agents.project_structure_agent import generate_structure

from executor.run_code import run_file
from utils.file_manager import (
    create_project,
    save_file,
    save_readme,
    create_file_structure
)

from utils.requirements_generator import generate_requirements
# from agents.frontend_agent import generate_frontend_structure, generate_frontend_code
from executor.run_project import run_backend
# from executor.browser_launcher import open_browser
from agents.qa_agent import generate_tests
from agents.api_test_agent import test_api
# from agents.devops_agent import generate_docker_setup, extract_docker_files
# from executor.docker_runner import run_docker
from agents.product_manager_agent import create_product_spec
# from agents.devops_agent import generate_docker_setup
import ast
import re

FILE_PRIORITY = {
    "models": 1,
    "database": 1,
    "schemas": 2,
    "services": 2,
    "routes": 3,
    "controllers": 3,
    "main": 4
}

MAX_IMPROVEMENTS = 3
MAX_RETRIES = 3

def clean_code(code):
    code = re.sub(r"```\w*", "", code)  # ```python, ```json, ```sql sab hatega
    code = code.replace("```", "")
    
    garbage = [
        "Here is the corrected code:",
        "Here is the code:",
        "The corrected code is:",
        "Sure! Here is",
        "Explanation:",
        "Here's"
    ]
    for g in garbage:
        code = code.replace(g, "")
    
    return code.strip()

def validate_python(code):

    try:
        ast.parse(code)
        return True, None

    except SyntaxError as e:
        return False, str(e)
    
def get_priority(file):

    for key in FILE_PRIORITY:
        if key in file:
            return FILE_PRIORITY[key]

    return 10
def run():

    prompt = input("What do you want to build? ")

    print("\nStarting AI Dev Agent Controller...")
    
    run_company(prompt)
    
def run_company(prompt):

    print("Product Manager analyzing idea...")

    spec = create_product_spec(prompt)

    print("\nProduct Specification:\n")
    print(spec)

    print("\nEngineering team building project...")

    print("\nQA team generating tests...")

    tests = generate_tests(spec)

    create_file_structure(["tests/test_api.py"])

    save_file("generated_project", "tests/test_api.py", tests)
    print("Tests created.")
    """
    print("\nDevOps preparing deployment...")

    docker = generate_docker_setup(prompt)

    print("Docker setup ready.")
    """
    print("\nAI Software Company finished the project.")
    
    print("\nSelecting tech stack...")

    stack = select_stack(prompt)

    print("\nSelected Stack:\n", stack)

    print("\nGenerating project structure...")

    structure = generate_structure(prompt)

    # 🔧 CLEAN AI OUTPUT
    structure = structure.replace("```", "")
    structure = structure.replace("Here is the folder structure you requested:", "")
    structure = structure.replace("Here is the folder structure:", "")
    structure = structure.strip()

    print("\nAI GENERATED STRUCTURE:\n")
    print(structure)

    files = [
        f.strip()
        for f in structure.split("\n")
        if "/" in f and not f.startswith("/")
    ]
    
    print("\nGenerated Structure:")

    for f in files:
        print(f)

    create_project("generated_project")

    files = [f"generated_project/{f}" for f in files]
    create_file_structure(files)
    """
    print("\nGenerating React frontend structure...")

    frontend_structure = generate_frontend_structure(prompt)

    frontend_files = [
        f.strip().replace("-", "")
        for f in frontend_structure.split("\n")
        if "/" in f
    ]
    print("\nFrontend Structure:")

    for f in frontend_files:
        
        f = f.strip()

        if not f:
            continue

        print(f)

    create_file_structure(frontend_files)
 
    print("\nGenerating frontend code...")

    for file in frontend_files:

        file = file.strip()

        if not file:
            continue

        print("Coding:", file)

        try:

            code = generate_frontend_code(file, prompt)

            code = code.replace("```javascript", "")
            code = code.replace("```jsx", "")
            code = code.replace("```", "")

            save_file(file, code)

        except Exception as e:

            print("Error generating frontend code:", e)
    """
    

    print("\nPlanning project...")

    plan = create_plan(prompt)

    files = []

    for line in plan.split("\n"):

        line = line.strip().replace("`","").replace("#","")

        if not line:
            continue

        # skip directories
        if line.endswith("/"):
            continue

        # ignore python cache folders
        if "__pycache__" in line:
            continue

        # skip non-file text lines
        if "." not in line and "/" not in line:
            continue
        
        if line.endswith(("backend","models","utils")):
            continue

        if line.startswith(("backend/","frontend/","database/")):
            files.append(line)

        elif line.endswith((".py",".txt",".env",".gitignore",".json",".sql")):
            files.append(line)

    # 🔥 dependency order
    files = list(set(files))
    files = sorted(files, key=get_priority)

    print("\nGenerated Plan:\n")
    print(plan)

    for file in files:

        print("Generating:", file)

        if file == "logging.py":
            file = "logger.py"

        code = generate_code(file, prompt)

        code = clean_code(code)
        
        # fix backend imports
        code = code.replace("from backend.", "from ")
        code = re.sub(r"from \.([\w]+)", r"from \1", code)
        code = code.replace("import backend.", "import ")

        if not code.strip():
            print("Empty code generated for", file)
            continue

        valid, error = validate_python(code)

        if not valid:
            print("Syntax error detected before execution:", error)

            fixed_code = debug_code(code, error)
            fixed_code = clean_code(fixed_code)
            
            fixed_code = fixed_code.replace("from backend.", "from ")
            fixed_code = fixed_code.replace("import backend.", "import ")
            
            code = fixed_code

            valid, error = validate_python(code)

            if not valid:
                print("Still invalid after fix:", error)
                continue

        path = save_file("generated_project", file, code)

        # Only run python files
        if file.endswith(".py") and file in ["main.py", "app.py"]:

            for attempt in range(MAX_RETRIES):

                stdout, stderr = run_file(path)

                if not stderr or "Warning" in stderr:
                    print("Code working:", file)
                    break

                print(f"Error detected fixing... Attempt {attempt+1}/{MAX_RETRIES}")
                print("\nERROR LOG:\n", stderr)

                source_code = open(path).read()

                debug_prompt = f"""
                File: {file}

                Code:
                {source_code}

                Error:
                {stderr}

                Fix the code. Return ONLY valid Python code.
                """

                fixed_code = debug_code(debug_prompt, stderr)

                fixed_code = clean_code(fixed_code)

                fixed_code = fixed_code.replace("from backend.", "from ")
                fixed_code = fixed_code.replace("import backend.", "import ")

                path = save_file("generated_project", file, fixed_code)

            # infinite loop stop
            if stderr and attempt == MAX_RETRIES - 1:
                print("Skipping file due to repeated errors:", file)

    print("\nProject generated!")
    
    print("Starting backend server...")

    project_path = "workspace/generated_projects/generated_project"

    generate_requirements(project_path)

    print("requirements.txt generated")

    print("\nGenerating README...")

    readme = generate_readme(prompt)

    save_readme(readme)

    print("README created.")

    print("\nRunning backend server...")

    print("Testing API...")

    test_api()

    print("Generating tests...")

    tests = generate_tests(prompt)
    
    create_file_structure(["tests/test_api.py"])

    save_file("generated_project","tests/test_api.py", tests)

    print("Tests created.")
    """
    print("Generating Docker setup...")

    docker_output = generate_docker_setup(prompt)

    dockerfile, compose = extract_docker_files(docker_output)

    save_file("Dockerfile", dockerfile)

    save_file("docker-compose.yml", compose)
    """ 
    print("\nLaunching generated application...")

    try:

        project_path = "workspace/generated_projects/generated_project"
        run_backend(project_path)

        # run_frontend()

        # open_browser()

    except Exception as e:

        print("Error running project:", e)

if __name__ == "__main__":

    prompt = input("What product do you want to build? ")

    run_company(prompt)