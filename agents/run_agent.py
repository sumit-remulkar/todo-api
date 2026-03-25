import subprocess
import webbrowser
import time
from core.logger import log

def run_backend():

    process = subprocess.Popen(
        ["uvicorn", "backend.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return process

def run_project():
    
    log("🚀 Starting generated application")

    subprocess.Popen(
        ["uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd="workspace/generated_projects/generated_project"
    )

    time.sleep(3)

    webbrowser.open("http://127.0.0.1:8000/docs")