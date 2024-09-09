"""Pydantic based base classes."""

# Standard Library
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, Type, Union

# 3rd party libraries
from pydantic import (
    BaseModel,
    ConfigDict,
    PlainSerializer,
    SecretStr,
    ValidationError,
)
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
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


class OnclusiveEnvSettingsSource(EnvSettingsSource):
    """Custom environement variable settings source."""

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        """Overrides the get_field_value method to allow for multiple prefixes to cohexist."""
        if field_name in self.settings_cls.model_fields:
            env_name = (
                self.settings_cls._get_base_class(field_name).model_config["env_prefix"]
                + field_name
            ).lower()
            return self.env_vars.get(env_name), field_name, False
        else:
            return super().get_field_value(field, field_name)


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
            message: str = "Missing environment variables"
            env_vars: List[str] = []
            for err in e.errors():
                env_prefix: str = __pydantic_self__._get_base_class(
                    err["loc"][0]
                ).model_config["env_prefix"]
                env_var = f"{env_prefix.upper()}{err['loc'][0].upper()}"
                env_vars.append(env_var)
            raise ValueError(f"{message}: {str(env_vars)}")

    @classmethod
    def _get_base_class(cls, field_name: str) -> Type[BaseSettings]:
        """Returns the base class this class inherited a field from.

        Args:
            field_name (str): pydantic settings field name
        """
        bases: Iterable[BaseSettings] = cls.__bases__
        for base in bases:
            try:
                value = base.model_fields.get(field_name)
                if value is not None:
                    return base
            except Exception:
                continue
        return cls

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for loading the settings values.
        """
        return (
            init_settings,
            OnclusiveEnvSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )


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
