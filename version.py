import subprocess
from datetime import datetime


def get_git_info():
    try:
        # Get the short Git hash
        git_hash = (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )

        # Get the latest commit date
        git_date = (
            subprocess.check_output(["git", "log", "-1", "--format=%cd", "--date=iso"])
            .decode("ascii")
            .strip()
        )
        commit_date = datetime.strptime(git_date, "%Y-%m-%d %H:%M:%S %z").strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return f"{git_hash} ({commit_date})"
    except subprocess.CalledProcessError:
        return "Unknown"


__version__ = get_git_info()
