from gitsnap.git_runner import run_git

def get_repo_info(path):
    root = run_git(["rev-parse", "--show-toplevel"], path)
    name = root.split("/")[-1]
    branch = run_git(["branch", "--show-current"], path)
    return{"name": name, "branch": branch}

def get_recent_commits(path, n=10):
   raw_output = run_git(
    ["log", "-n", str(n), "--pretty=format:%h|%an|%ar|%s"],
    path,
   )
   lines = raw_output.splitlines()
   commits = []
   for line in lines:
        if not line:
            continue
        branchs = line.split("|")
        commits.append({
            "hash": branchs[0],
            "author": branchs[1],
            "date": branchs[2],
            "message": branchs[3],
            
        })
    return commits