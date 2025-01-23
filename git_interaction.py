import os
import subprocess

def commit_and_push_to_github(file_path, commit_message):
    """
    Commits the specified file to the local Git repository and pushes it to GitHub.

    Args:
        file_path: Path to the file to be committed.
        commit_message: Commit message for the Git commit.
    """

    try:
        # Stage the file for commit
        subprocess.run(["git", "add", file_path])

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message])

        # Push changes to the remote repository
        subprocess.run(["git", "push", "origin", "main"])  # Assuming your default branch is 'main'

        print(f"File '{file_path}' committed and pushed to GitHub successfully!")

    except Exception as e:
        print(f"Error committing and pushing to GitHub: {e}")

# Example usage:
file_path = "C:\Users\User\OneDrive - Ngee Ann Polytechnic\Ngee Ann Poly\YEAR 2 SEM 2\DDP\ASSG2\ddp_data.csv"
commit_message = "Updated bus arrival data"
commit_and_push_to_github(file_path, commit_message)
