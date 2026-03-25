import json
import os

MEMORY_FILE = "memory/project_context.json"

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {"files": []}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_file(filename):

    memory = load_memory()

    if filename not in memory["files"]:
        memory["files"].append(filename)

    save_memory(memory)


def get_files():

    memory = load_memory()

    return memory.get("files", [])