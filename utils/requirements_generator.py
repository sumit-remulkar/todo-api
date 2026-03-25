import os
import re


def generate_requirements(project_path):

    imports = set()

    for root, dirs, files in os.walk(project_path):
        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                with open(path, "r") as f:
                    content = f.read()

                matches = re.findall(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)

                for m in matches:
                    imports.add(m)

    # remove built-in libraries
    ignore = {
        "os","sys","re","json","math","subprocess",
        "datetime","time","random"
    }

    packages = [pkg for pkg in imports if pkg not in ignore]

    req_file = os.path.join(project_path, "requirements.txt")

    with open(req_file, "w") as f:
        for pkg in packages:
            f.write(pkg + "\n")

    return packages