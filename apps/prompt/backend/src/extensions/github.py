"""Github connector."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
from github import Auth, GithubIntegration
from pydantic import SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenModel

# Source
from src.settings import get_settings


settings = get_settings()


class GithubClient(OnclusiveFrozenModel):
    """Github client wrapper class."""

    app_id: str
    app_private_key: SecretStr
    repo_url: str
    excluded_files: List[str] = [".gitkeep", "README.md", ".gitignore"]

    @property
    def repo(self) -> Any:
        """Set github connector."""
        auth = Auth.AppAuth(self.app_id, self.app_private_key.get_secret_value())
        gi = GithubIntegration(auth=auth)
        installation = gi.get_installations()[0]
        g = installation.get_github_for_installation()
        return g.get_repo(self.repo_url)

    def write(self, path: str, commit: str, contents: str = "") -> Dict:
        """Creates folder."""
        return self.repo.create_file(path, commit, contents)

    def read(self, path: str) -> Any:
        """Opens file."""
        contents = self.repo.get_contents(path)
        if isinstance(contents, list):
            return [self.read(content.path) for content in contents]
        result: str = ""
        if contents.type == "file":
            result = contents.decoded_content.decode()
        return result

    def update(self, path: str, commit_message: str, template: str) -> Dict:
        """Updates a file if it exists."""
        try:
            file_contents = self.repo.get_contents(path)
            return self.repo.update_file(
                file_contents.path, commit_message, template, file_contents.sha
            )
        except Exception as e:
            raise FileNotFoundError(f"File at path {path} not found: {e}")

    def ls(self, path: str) -> List[str]:
        """Recursively list files."""
        contents = self.repo.get_contents(path)
        result: List[str] = []
        for content_file in contents:
            if content_file.type == "dir" and all(
                f not in content_file.path for f in self.excluded_files
            ):
                result.append(content_file.path)
                result.extend(self.ls(content_file.path))
            if content_file.type == "file" and all(
                f not in content_file.name for f in self.excluded_files
            ):
                result.append(content_file.path)
        return result

    def exists(self, path: str) -> bool:
        """Check if a file or folder exists in the repo."""
        try:
            self.repo.get_contents(path)
            return True
        except Exception:
            return False
    
    def rm(self, path: str, commit: str) -> None:
        """Removes content from repo."""
        contents = self.repo.get_contents(path)
        if not isinstance(contents, list):
            return self.repo.delete_file(contents.path, commit, contents.sha)
        for content_file in contents:
            if content_file.type == "dir":
                sub_contents = self.repo.get_contents(content_file.path)
                for sub_content_file in sub_contents:
                    self.repo.delete_file(
                        sub_content_file.path, commit, sub_content_file.sha
                    )
            else:
                self.repo.delete_file(content_file.path, commit, content_file.sha)


github = GithubClient(
    app_id=settings.PROMPT_REGISTRY_APP_ID,
    app_private_key=settings.PROMPT_REGISTRY_APP_PRIVATE_KEY,
    repo_url=settings.GITHUB_REPOSITORY,
)
