import os
import subprocess
from typing import List, Union

class GitOperations:
    def __init__(self, repo_path: str = "."):
        """Initialize GitOperations with repository path."""
        self.repo_path = os.path.abspath(repo_path)

    def _run_git_command(self, command: List[str]) -> tuple[int, str, str]:
        """Run a git command and return the result."""
        process = subprocess.Popen(
            command,
            cwd=self.repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def add_files(self, files: Union[str, List[str]]) -> tuple[bool, str]:
        """Add files to git staging."""
        if isinstance(files, str):
            files = [files]
        
        returncode, stdout, stderr = self._run_git_command(['git', 'add'] + files)
        success = returncode == 0
        message = stderr if stderr else stdout
        return success, message

    def commit(self, message: str) -> tuple[bool, str]:
        """Commit staged changes."""
        returncode, stdout, stderr = self._run_git_command(['git', 'commit', '-m', message])
        success = returncode == 0
        message = stderr if stderr else stdout
        return success, message

    def delete_file(self, file_path: str, commit: bool = False) -> tuple[bool, str]:
        """Delete a file and optionally commit the change."""
        if not os.path.exists(os.path.join(self.repo_path, file_path)):
            return False, f"File {file_path} does not exist"

        try:
            # Remove file from git and filesystem
            returncode, stdout, stderr = self._run_git_command(['git', 'rm', file_path])
            success = returncode == 0
            message = stderr if stderr else stdout

            if success and commit:
                commit_success, commit_message = self.commit(f"Deleted {file_path}")
                if not commit_success:
                    return False, f"File removed but commit failed: {commit_message}"
                message += f"\n{commit_message}"

            return success, message
        except Exception as e:
            return False, str(e) 