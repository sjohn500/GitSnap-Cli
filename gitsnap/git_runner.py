import subprocess
from gitsnap.exceptions import GitNotFoundError, GitCommandError

DELIMITER = "---GITSNAP_COMMIT_START---"


def run_git(args: list[str], cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            raise GitCommandError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout.strip()
    except FileNotFoundError:
        raise GitNotFoundError("Git is not installed or PATH is not found")


def build_trace_args(limit: int = 30, delimiter: str = DELIMITER) -> list[str]:
    fields = ["%H", "%an", "%ar", "%s"]
    # Put delimiter at the START so each commit header + its file list stay in one block
    format_spec = f"{delimiter}%n{'|'.join(fields)}"

    return [
        "log",
        "-n",
        str(limit),
        f"--pretty=format:{format_spec}",
        "--name-status",
        "--find-renames",
    ]


def split_commit_blocks(raw_output: str, delimiter: str = DELIMITER) -> list[str]:
    if not raw_output:
        return []
    blocks = []
    for chunk in raw_output.split(delimiter):
        cleaned = chunk.strip()
        if cleaned:
            blocks.append(cleaned)
    return blocks


def parse_commit_block(block: str) -> dict | None:
    lines = [line for line in block.splitlines() if line.strip()]
    if not lines:
        return None

    header_line = lines[0].split("|", 3)
    if len(header_line) < 4:
        return None

    commit_hash, author, rel_date, subject = [field.strip() for field in header_line]

    files = []
    for line in lines[1:]:
        parts = line.split("\t")
        status = parts[0]

        if status.startswith(("R", "C")) and len(parts) >= 3:
            files.append({
                "status": status,
                "old_path": parts[1],
                "new_path": parts[2],
            })
        elif len(parts) >= 2:
            files.append({
                "status": status,
                "path": parts[1],
            })

    return {
        "hash": commit_hash,
        "author": author,
        "relative_date": rel_date,
        "subject": subject,
        "files": files,
    }


def get_commit_history(cwd: str, limit: int = 30) -> list[dict]:
    args = build_trace_args(limit=limit, delimiter=DELIMITER)
    raw_output = run_git(args, cwd=cwd)
    blocks = split_commit_blocks(raw_output, delimiter=DELIMITER)
    
    commits = []
    for block in blocks:
        parsed = parse_commit_block(block)
        if parsed:
            commits.append(parsed)
    return commits
