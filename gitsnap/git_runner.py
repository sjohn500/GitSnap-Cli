import subprocess
from gitsnap.exceptions import GitNotFoundError, GitCommandError

def run_git(arg, cwd):
    try:
        result = subprocess.run(["git"] + arg, capture_output=True, text=True, cwd=cwd, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            raise GitCommandError(f"git {' '.join(arg)} failed: {result.stderr}")
        return result.stdout.strip()
         
    except FileNotFoundError:
        raise GitNotFoundError("Git is not installed or PATH is not Found")