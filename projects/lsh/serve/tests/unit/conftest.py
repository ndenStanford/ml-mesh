"""Conftest."""

# Standard Library
from typing import Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    # Source
    from src.app import app

    return app


@pytest.fixture()
def test_client(app: FastAPI) -> Generator[TestClient, None, None]:
    yield TestClient(app=app)


@pytest.fixture
def example_content_input() -> str:
    content = "Call functions to generate hash signatures for each article"
    return content


@pytest.fixture
def example_lsh_output() -> str:
    output = [
        "AAAAADWCEZ4AAAAAUtj2YwAAAABdPg5BAAAAAGrzluAAAAAAGN7zAQ==",
        "AAAAAK8jTm4AAAAA9nYYaQAAAACJngRPAAAAAKy8wYsAAAAAVWN4Hw==",
        "AAAAADuLk0EAAAAABdQyawAAAABsuvhdAAAAAA1DABQAAAAAh9d+YA==",
        "AAAAAECJCqoAAAAAHUPpyQAAAAAg+H6KAAAAADaxXSQAAAAAJLxnCQ==",
        "AAAAAGL169oAAAAAR2FhiQAAAAB2Va+CAAAAADCxTHMAAAAAAjECCg==",
        "AAAAAE6Xf7MAAAAAcLTJOAAAAAAZARdnAAAAADC5/D4AAAAARNwyWA==",
        "AAAAAD6p5OUAAAAAJNpVRAAAAAAyjKv2AAAAAFy5Ny4AAAAAQY+4YQ==",
        "AAAAACOM9ZQAAAAAW6a+cAAAAAAJJ73aAAAAAAtnQgYAAAAAc4I7eA==",
        "AAAAADrT01MAAAAARaZvQwAAAADIGgsAAAAAAFOfbL0AAAAAVn8nnA==",
        "AAAAAJ4+Da8AAAAA/AEiWQAAAACOCFimAAAAACZAFWIAAAAApx5IZg==",
        "AAAAABx520cAAAAAQ0uewQAAAAB4LCByAAAAAC0HtLYAAAAApdISrQ==",
        "AAAAAD+W5aIAAAAAkXOTeAAAAAAV2dHhAAAAAGaYjA0AAAAAVxfubQ==",
        "AAAAAGngXcUAAAAAJKJO/gAAAACqDxLQAAAAAD//H6QAAAAAJ3cBfw==",
        "AAAAAO4e9uwAAAAAC4Lm/QAAAABsxREiAAAAAB1C4ocAAAAADb4t7A==",
        "AAAAADJ0nxwAAAAAEDygXwAAAAAGK095AAAAAFOHdZ0AAAAAVbu+HA==",
        "AAAAAEp51s0AAAAA3E6ZnQAAAABu56QrAAAAACn2/tsAAAAA19cjFg==",
        "AAAAAKgaBv4AAAAABK518AAAAACE0OvYAAAAAFdOrMkAAAAANYMbXA==",
        "AAAAAEbcylcAAAAA5gu9RQAAAAB16U20AAAAAH+6Z+IAAAAASoheqw==",
        "AAAAAGh06l4AAAAAOLbR1gAAAAAYVGwgAAAAACJBFwYAAAAAL0adJw==",
        "AAAAAAU+nl4AAAAAsW2HuwAAAACegI2kAAAAACFofK0AAAAAFm7yPA==",
        "AAAAADkC7xwAAAAACQOFpwAAAABV6fAWAAAAAHJEdacAAAAADG34cw==",
        "AAAAAFgLz+IAAAAADLRZHwAAAAAJwDGyAAAAAB1zKkcAAAAAbKUEUQ==",
        "AAAAAE0nIp0AAAAAa0LQkwAAAAAp3f3kAAAAAJDTEWgAAAAANEIcig==",
        "AAAAABLE06gAAAAANvgiYQAAAAA08Z7IAAAAAFAyPWEAAAAAfEWuKw==",
        "AAAAAJH+RZYAAAAATNnjqAAAAAAvn/v3AAAAAHLDmC8AAAAAB1tjLw==",
    ]
    return output
