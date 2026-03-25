import re
from core.llm import get_llm
from core.logger import log

llm = get_llm()


def generate_docker_setup(project_prompt):

    prompt = f"""
You are a DevOps engineer.

Create Docker setup for the following project.

Project:
{project_prompt}

Generate:

1. Dockerfile
2. docker-compose.yml

Return code blocks for each file.
"""

    response = llm.invoke(prompt)

    response = str(response)

    return response

def extract_docker_files(text):

    dockerfile = ""
    compose = ""

    docker_match = re.search(r"Dockerfile(.*?)```", text, re.S)
    compose_match = re.search(r"docker-compose.yml(.*?)```", text, re.S)

    if docker_match:
        dockerfile = docker_match.group(1)

    if compose_match:
        compose = compose_match.group(1)

    return dockerfile.strip(), compose.strip()

def run(state):
    log("🐳 Generating Docker setup")
    prompt = state["prompt"]

    docker_text = generate_docker_setup(prompt)

    dockerfile, compose = extract_docker_files(docker_text)

    return {
        "dockerfile": dockerfile,
        "docker_compose": compose
    }


def generate(state):
    return run(state)