import subprocess


def run_docker():

    subprocess.run(["docker", "compose", "up", "--build"])