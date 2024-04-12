"""Github connector."""

# Standard Library
import json
from typing import Any, Dict, List, Optional

# 3rd party libraries
from github import Github
from github.ContentFile import ContentFile

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSchema

# Source
from src.settings import get_settings


settings = get_settings()


class GithubClient(OnclusiveFrozenSchema):
    """Github client wrapper class."""

    access_token: str
    repo_url: str
    excluded_files: List[str] = [".gitkeep"]

    @property
    def repo(self) -> Any:
        """Set github connector."""
        g = Github(self.access_token)
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
                sub_contents = repo.get_contents(content_file.path)
                result.extend(self.ls(self.repo, sub_contents))
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
    access_token=settings.GITHUB_TOKEN.get_secret_value(), repo_url=settings.GITHUB_URL
)
