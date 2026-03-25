import subprocess

def run_tests():

    result = subprocess.run(
        ["pytest"],
        capture_output=True,
        text=True
    )

    return result.stdout, result.stderr