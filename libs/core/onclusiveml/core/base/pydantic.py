"""Pydantic based base classes."""

# Standard Library
from pathlib import Path
from typing import Any, List, Optional, Tuple, Type, Union

# 3rd party libraries
from pydantic import (
    BaseModel,
    ConfigDict,
    PlainSerializer,
    SecretStr,
    ValidationError,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import (
    ENV_FILE_SENTINEL,
    CliSettingsSource,
    DotenvType,
)
from typing_extensions import Annotated

# Internal libraries
from onclusiveml.core.base.exception import BaseClassNotFound


OnclusiveSecretStr = Annotated[
    SecretStr, PlainSerializer(lambda x: x.get_secret_value(), return_type=str)
]


class OnclusiveBaseSettings(BaseSettings):
    """Base class for all parameter classes in the core library."""

    model_config = SettingsConfigDict(
        extra="forbid",
        env_file_encoding="utf-8",
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    def __init__(
        __pydantic_self__,
        _case_sensitive: Optional[bool] = None,
        _env_prefix: Optional[str] = None,
        _env_file: Optional[DotenvType] = ENV_FILE_SENTINEL,
        _env_file_encoding: Optional[str] = None,
        _env_ignore_empty: Optional[bool] = None,
        _env_nested_delimiter: Optional[str] = None,
        _env_parse_none_str: Optional[str] = None,
        _env_parse_enums: Optional[bool] = None,
        _cli_prog_name: Optional[str] = None,
        _cli_parse_args: Optional[Union[bool, List[str], Tuple[str, ...]]] = None,
        _cli_settings_source: Optional[CliSettingsSource[Any]] = None,
        _cli_parse_none_str: Optional[str] = None,
        _cli_hide_none_type: Optional[bool] = None,
        _cli_avoid_json: Optional[bool] = None,
        _cli_enforce_required: Optional[bool] = None,
        _cli_use_class_docs_for_groups: Optional[bool] = None,
        _cli_prefix: Optional[str] = None,
        _secrets_dir: Optional[Union[str, Path]] = None,
        **values: Any,
    ) -> None:
        """Override initialisation to introduce verbose environment variable error message."""
        try:
            super().__init__(
                **__pydantic_self__._settings_build_values(
                    values,
                    _case_sensitive=_case_sensitive,
                    _env_prefix=_env_prefix,
                    _env_file=_env_file,
                    _env_file_encoding=_env_file_encoding,
                    _env_ignore_empty=_env_ignore_empty,
                    _env_nested_delimiter=_env_nested_delimiter,
                    _env_parse_none_str=_env_parse_none_str,
                    _env_parse_enums=_env_parse_enums,
                    _cli_prog_name=_cli_prog_name,
                    _cli_parse_args=_cli_parse_args,
                    _cli_settings_source=_cli_settings_source,
                    _cli_parse_none_str=_cli_parse_none_str,
                    _cli_hide_none_type=_cli_hide_none_type,
                    _cli_avoid_json=_cli_avoid_json,
                    _cli_enforce_required=_cli_enforce_required,
                    _cli_use_class_docs_for_groups=_cli_use_class_docs_for_groups,
                    _cli_prefix=_cli_prefix,
                    _secrets_dir=_secrets_dir,
                )
            )
        except ValidationError as e:
            # patch error locations, replacing the field name by the expected environment variable
            env_prefix: str = __pydantic_self__.__class__.model_config["env_prefix"]
            for err in e.errors():
                env_var = f"{env_prefix}{err['loc'][0].upper()}"
                err["loc"] = (env_var,)
            raise ValueError(err)


class OnclusiveFrozenSettings(OnclusiveBaseSettings):
    """Immutable Settings.

    After initialization, updating the attribute values
    will not be possible.
    """

    model_config = SettingsConfigDict(validate_default=True, frozen=True)


class OnclusiveBaseModel(BaseModel):
    """Base for all data models."""

    model_config = ConfigDict(
        extra="forbid", validate_assignment=True, from_attributes=True
    )


class OnclusiveFrozenModel(OnclusiveBaseModel):
    """Immutable data model."""

    model_config = ConfigDict(frozen=True)


def cast(
    obj: OnclusiveBaseSettings, t: Type[OnclusiveBaseSettings]
) -> OnclusiveBaseSettings:
    """Cast pydantic settings to parent class.

    Args:
        obj (OnclusiveBaseSettings): object to cast
        t: parent class
    """
    if t not in type(obj).__bases__:
        raise BaseClassNotFound(base=str(t), derived=type(obj))

    data = {k: getattr(obj, k) for k in t.schema().get("properties").keys()}

    return t(**data)
