"""Functionals."""

# Standard Library
from typing import Any

# Source
from src.model.tables import LanguageModel
from src.project.tables import Project
from src.prompt.tables import PromptTemplate


def generate(model: LanguageModel, prompt: PromptTemplate, **parameters: dict) -> str:
    """Generates from prompt.

    Args:
        model (LanguageModel):
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(prompt.template),
        ]
    )

    chain = prompt | model

    return chain.invoke(parameters)


def create_prompt(repo: Any, project: Project, prompt: PromptTemplate) -> None:
    """Create prompt template in github."""
    commit = repo.create_file(
        f"{project.alias}/{prompt.alias}.json",
        f"Add new prompt {prompt.alias}",
        prompt.json(exclude={"sha"}),
    )
    prompt.sha = commit["commit"].sha
    prompt.save()
