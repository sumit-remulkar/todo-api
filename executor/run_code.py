import subprocess
import sys

def run_file(file_path):

    print("Running file:", file_path)

    process = subprocess.run(
        [sys.executable, file_path],
        capture_output=True,
        text=True
    )

    return process.stdout, process.stderr