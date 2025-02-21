"""Service initialization."""

# Standard Library
from typing import List, Type

# 3rd party libraries
from botocore.exceptions import ClientError
from dyntastic import Dyntastic

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.system import SystemInfo

# Source
from src.extensions.github import github
from src.generated.tables import Generated
from src.model.constants import DEFAULT_MODELS
from src.model.tables import LanguageModel
from src.project.tables import Project
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_tables([LanguageModel, PromptTemplate, Project, Generated])
    _initialize_table(LanguageModel, DEFAULT_MODELS)
    logger.info("Finish tables initialization")
    if SystemInfo.in_docker():
        _syncronize_prompts()


def _create_tables(tables: List[Type[Dyntastic]]) -> None:
    """Create Tables."""
    for table in tables:
        try:
            table.create_table()
        except ClientError:
            logger.info("Table already exists, skipping creation ...")


def _initialize_table(table: Type[Dyntastic], values: List[dict]) -> None:
    """Initializes table."""
    for value in values:
        row = table.safe_get(value["alias"])
        if row is None:
            table(**value).save()


def _validate_prompts_to_sync(prompts_to_sync: List[str]):
    """Validate entries in PROMPTS_TO_SYNC to ensure they follow the 'folder/file' format.

    Args:
        prompts_to_sync (List[str]): List of prompt paths to validate.

    Raises:
        ValueError: If any entry does not contain a '/', or has an invalid folder or file name.
    """
    for prompt_path in prompts_to_sync:
        if "/" not in prompt_path:
            raise ValueError(
                f"Invalid entry in PROMPTS_TO_SYNC: {prompt_path}. Must be in 'folder/file' format."
            )
        folder, file = prompt_path.split("/", 1)
        if not folder.strip() or not file.strip():
            raise ValueError(
                f"Invalid entry in PROMPTS_TO_SYNC: {prompt_path}. Folder and file must be non-empty."
            )


def _syncronize_prompts():
    """Save prompts from registry in dynamoDB if non-exisant."""
    logger.info("Start prompt syncronization...")
    _validate_prompts_to_sync(settings.PROMPTS_TO_SYNC)
    files = github.ls("")
    for file in files:
        if file in settings.PROMPTS_TO_SYNC:
            project_alias, *prompt_alias = file.split("/")
            project = Project.safe_get(project_alias)
            if project is None:
                Project(alias=project_alias).sync()
            if project_alias != ".github" and len(prompt_alias) > 0:
                PromptTemplate(
                    alias=prompt_alias[0],
                    template=github.read(file),
                    project=project_alias,
                ).sync()
    logger.info("Finish prompt syncronization")
