"""Github connector."""

# Standard Library
import json
from typing import Any, Dict, List, Optional

# 3rd party libraries
from github import Auth, GithubIntegration
from pydantic import SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSchema

# Source
from src.settings import get_settings


settings = get_settings()


class GithubClient(OnclusiveFrozenSchema):
    """Github client wrapper class."""

    app_id: str
    app_private_key: SecretStr
    repo_url: str
    excluded_files: List[str] = [".gitkeep"]

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

    def read(self, path: str) -> Optional[Dict]:
        """Opens file."""
        contents = self.repo.get_contents(path)
        result: Optional[Dict] = None
        if contents.type == "file":
            result = json.loads(contents.decoded_content.decode())
        return result

    def ls(self, path: str) -> List[str]:
        """Recursively list files."""
        contents = self.repo.get_contents(path)
        result: List[str] = []
        for content_file in contents:
            if content_file.type == "dir":
                sub_contents = self.repo.get_contents(content_file.path)
                result.extend([s.path for s in sub_contents])
            if (
                content_file.type == "file"
                and content_file.name not in self.excluded_files
            ):
                result.append(content_file.path)
        return result

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
