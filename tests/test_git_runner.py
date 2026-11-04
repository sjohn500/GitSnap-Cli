"""Tests for the Git subprocess wrapper."""
import pytest
from gitsnap.git_runner import run_git
from gitsnap.exceptions import GitCommandError


def test_run_git_returns_output():
    result = run_git(["--version"], ".")
    assert result.startswith("git version")


def test_run_git_raises_on_bad_command():
    with pytest.raises(GitCommandError):
        run_git(["not-a-real-git-command"], ".")