"""Prompt injection validator."""

# Standard Library
import json
from typing import Any, Optional, Union  # noqa: F401

# ML libs
from transformers import AutoTokenizer, Pipeline, pipeline  # noqa: F401

# 3rd party libraries
from langchain_experimental.prompt_injection_identifier import (
    HuggingFaceInjectionIdentifier,
)
from optimum.onnxruntime import ORTModelForSequenceClassification
from pydantic import ValidationError

# Source
from src.prompt_validator.exceptions import PromptInjectionException


class PatchedHuggingFaceInjectionIdentifier(HuggingFaceInjectionIdentifier):
    """Patched HuggingFaceInjectionIdentifier using experimental fix.

    https://github.com/langchain-ai/langchain/discussions/19995
    """

    def __init__(self, **data: Any) -> None:
        try:
            super().__init__(**data)
        except ValidationError as pve:
            print(
                f"This is a warning. __init__ failed to validate:\n{json.dumps(data, indent=4)}"
            )
            print(f"This is the original exception:\n{pve.json()}")

    @classmethod
    def parse_obj(cls: Any, obj: Any) -> Any:
        """Overriden BaseModel's parse_obj method to allow Any type for cls and extra logging."""
        try:
            return super().parse_obj(obj)
        except ValidationError as pve:
            print(
                f"This is a warning. parse_obj failed to validate:\n{json.dumps(obj, indent=4)}"
            )
            print(f"This is the original exception:\n{pve.json()}")
            return None

    @classmethod
    def parse_raw(
        cls: Any,
        b: Any,
        *,
        content_type: Optional[str] = None,
        encoding: str = "utf8",
        proto: Any = None,
        allow_pickle: bool = False,
    ) -> Any:
        """Overriden BaseModel's parse_raw method to allow Any type for cls and extra logging."""
        try:
            return super().parse_raw(
                b=b,
                content_type=content_type,
                encoding=encoding,
                proto=proto,
                allow_pickle=allow_pickle,
            )
        except ValidationError as pve:
            print(f"This is a warning. parse_raw failed to validate:\n{b}")
            print(f"This is the original exception:\n{pve.json()}")
            return None


class PromptInjectionValidator:
    """Prompt Injection validation class to detect if prompts have been tampered with."""

    def __init__(
        self,
        model_path: str = "protectai/deberta-v3-base-prompt-injection-v2",
        revision: Optional[str] = None,
        max_length: int = 512,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            revision=revision,
            model_input_names=["input_ids", "attention_mask"],
        )
        self.model = ORTModelForSequenceClassification.from_pretrained(
            model_path, revision=revision, subfolder="onnx"
        )
        self.classifier = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            truncation=True,
            max_length=max_length,
        )
        self.injection_identifier = PatchedHuggingFaceInjectionIdentifier(
            model=self.classifier
        )

    def validate_prompt(self, prompt: str) -> Union[str, PromptInjectionException]:
        """Validate prompt to identify prompt injections."""
        try:
            return self.injection_identifier.run(prompt)
        except ValueError:
            raise PromptInjectionException(
                prompt=prompt,
            )
