"""Github connector."""

# 3rd party libraries
from github import Github

# Source
from src.settings import get_settings


settings = get_settings()


class GithubClient:
    """Github client wrapper class."""

    def get_repo(self) -> None:
        """Set github connector."""
        access_token = settings.GITHUB_TOKEN.get_secret_value()
        g = Github(access_token)
        repo_url = settings.GITHUB_URL
        return g.get_repo(repo_url)


github_repo = GithubClient().get_repo()
