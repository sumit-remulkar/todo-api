import subprocess

def push_to_github(repo_url):

    subprocess.run(["git","init"])
    subprocess.run(["git","add","."])
    subprocess.run(["git","commit","-m","AI generated project"])
    subprocess.run(["git","branch","-M","main"])
    subprocess.run(["git","remote","add","origin", repo_url])
    subprocess.run(["git","push","-u","origin","main"])