import os
import subprocess
from dotenv import load_dotenv
from github import Github

# load env variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def push_project(repo_name, project_path):

    # connect GitHub
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    # create repo
    repo = user.create_repo(repo_name)

    repo_url = repo.clone_url

    print("GitHub repo created:", repo_url)

    # go to project folder
    os.chdir(project_path)

    # initialize git
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "AI generated project"])
    subprocess.run(["git", "branch", "-M", "main"])

    # connect remote repo
    subprocess.run(["git", "remote", "add", "origin", repo_url])

    # push code
    subprocess.run(["git", "push", "-u", "origin", "main"])

    print("Project pushed to GitHub")

    return repo.html_url