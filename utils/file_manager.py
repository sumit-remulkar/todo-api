from core.memory import add_file
import os

BASE_PATH = os.path.abspath("workspace/generated_projects")

def create_file_structure(files):

    for file in files:

        file = file.strip()

        if not file:
            continue

        path = os.path.join(BASE_PATH, file)

        folder = os.path.dirname(path)

        os.makedirs(folder, exist_ok=True)

        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")

WORKSPACE = "workspace/generated_projects"

def create_project(name):

    path = f"workspace/generated_projects/{name}"

    os.makedirs(path, exist_ok=True)

    return path


def save_file(project, filename, code):

    project_path = os.path.join(WORKSPACE, project)

    os.makedirs(project_path, exist_ok=True)

    file_path = os.path.join(project_path, filename)

    # 🔥 Ensure folder exists
    folder = os.path.dirname(file_path)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "w") as f:
        f.write(code)

    return file_path

def save_readme(content):

    path = "workspace/generated_projects/README.md"

    with open(path, "w") as f:
        f.write(content)

    return path