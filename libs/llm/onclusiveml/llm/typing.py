"""Typing."""

# Standard Library
from typing import Union

# 3rd party libraries
from langchain.llms import BaseLLM
from langchain.prompts import BasePromptTemplate


LangchainT = Union[BaseLLM, BasePromptTemplate]
