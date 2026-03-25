import subprocess
import os


class RunResult:

    def __init__(self, success=True, error=None):

        self.success = success
        self.error = error


def run_backend(project_path):

    if not os.path.exists(project_path):
        return RunResult(success=False, error="Backend folder not found")

    print("\nStarting backend server...")

    try:

        process = subprocess.Popen(
            ["uvicorn", "main:app", "--reload", "--port", "8000"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return RunResult(success=True)

    except Exception as e:

        return RunResult(success=False, error=str(e))


def run_frontend(project_path):

    frontend_path = os.path.join(project_path, "frontend")

    if not os.path.exists(frontend_path):
        print("Frontend folder not found")
        return

    print("\nInstalling frontend dependencies...")

    subprocess.run(
        ["npm", "install"],
        cwd=frontend_path
    )

    print("\nStarting React frontend...")

    subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_path
    )


def run(project_path):

    try:

        result = run_backend(project_path)

        if not result.success:
            return result

        run_frontend(project_path)

        return RunResult(success=True)

    except Exception as e:

        return RunResult(success=False, error=str(e))