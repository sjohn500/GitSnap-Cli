from gitsnap.git_runner import run_git

def get_repo_info(path):
    root = run_git(["rev-parse", "--show-toplevel"], path)
    name = root.split("/")[-1]
    branch = run_git(["branch", "--show-current"], path)
    return{"name": name, "branch": branch}
