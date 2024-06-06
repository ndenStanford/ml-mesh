"""Typing."""

# Standard Library
from typing import Union

# 3rd party libraries
from langchain.prompts import BasePromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel


LangchainT = Union[BaseChatModel, BasePromptTemplate]
