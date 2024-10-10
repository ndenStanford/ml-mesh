"""From settings."""

# Standard Library
import collections
import inspect
import logging
from abc import ABC, abstractmethod
from inspect import Parameter, signature
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings


T = TypeVar("T")
_NO_DEFAULT = Parameter.empty

logger = logging.getLogger(__name__)


class FromSettings(ABC):
    """Mixin to give a from_settings method to classes."""

    @classmethod
    def from_settings(
        cls: Type[T],
        settings: OnclusiveBaseSettings,
        constructor_to_call: Callable[..., T] = None,
        constructor_to_inspect: Union[Callable[..., T], Callable[[T], None]] = None,
        **extras,
    ) -> Optional[T]:
        """
        This is the automatic implementation of `from_settings`. Any class that subclasses
        `FromSettings` gets this implementation for free.
        If you want your class to be instantiated from settings in the "obvious" way
        -- pop off parameters and hand them to your constructor with the same names --
        this provides that functionality.
        If you need more complex logic in your from `from_settings` method, you'll have to implement
        your own method that overrides this one.
        Example:
            class FeatureStore(BaseFeatureStore):
                def __init__(self,
                )
        """
        if settings is None:
            return None

        if not isinstance(settings, OnclusiveBaseSettings):
            raise ConfigurationError(
                "from_settings was passed a `settings` object that was not a `OnclusiveBaseSettings`."
                f"This happened when constructing an object of type {cls}."
            )
        # This is not a base class, so convert our settings and extras into a dict of kwargs.
        # See the docstring for an explanation of what's going on here.
        if not constructor_to_inspect:
            constructor_to_inspect = cls.__init__
        if not constructor_to_call:
            constructor_to_call = cls

        if constructor_to_inspect == object.__init__:
            # This class does not have an explicit constructor, so don't give it any kwargs.
            # Without this logic, _create_kwargs will look at object.__init__ and see that
            # it takes *args and **kwargs and look for those.
            kwargs: Dict[str, Any] = {}
        else:
            # This class has a constructor, so create kwargs for it.
            constructor_to_inspect = cast(Callable[..., T], constructor_to_inspect)
            kwargs = _create_kwargs(constructor_to_inspect, cls, settings, **extras)
        return constructor_to_call(**kwargs)  # type: ignore

    @property
    def settings(self) -> OnclusiveBaseSettings:
        """Returns settings."""
        return self._settings()

    def _settings(self) -> OnclusiveBaseSettings:
        """Internal method to returns the settings object.

        Should be overriden if the associated settings object is needed
        to be accessed via this class instance.
        """
        raise NotImplementedError()


def __infer_method_signature(cls: Type[T], method: Callable) -> Dict[str, Parameter]:
    """Infer method signature."""
    signature = inspect.signature(method)
    parameters = dict(signature.parameters)
    has_kwargs: bool = False
    var_positional_key = None

    for parameter in parameters.values():
        if parameter.kind == parameter.VAR_KEYWORD:
            has_kwargs = True
        elif parameter.kind == parameter.VAR_KEYWORD:
            var_positional_key = parameter.name

    if var_positional_key:
        del parameters[var_positional_key]

    if not has_kwargs:
        return parameters
    # "mro" is "method resolution order". The first one is the current class, the next is the
    # first superclass, and so on. We take the first superclass we find that inherits from
    # FromSettings.
    super_class = None
    for super_class_candidate in cls.mro()[1:]:
        if issubclass(super_class_candidate, FromSettings):
            super_class = super_class_candidate
            break

    if super_class:
        super_parameters = __infer_method_signature(super_class, super_class.__init__)
    else:
        super_parameters = dict()

    return {**super_parameters, **parameters}


def __can_construct_from_settings(t: Type) -> bool:
    """Check if class can be contructed via `from_settings` method."""
    if t in [str, int, float, bool]:
        return True
    origin = getattr(t, "__origin__", None)
    if hasattr(t, "from_settings"):
        return True
    args = getattr(t, "__args__")
    return all(__can_construct_from_params(arg) for arg in args)
    return hasattr(t, "from_settings")


def __create_extras(cls: Type[T], extras: Dict[str, Any]) -> Dict[str, Any]:
    """Given a dictionary of extra keyword arguments, returns a dictionary
    as kwargs thta actually are a part of the signature of cls.from_settings
    (or cls) method.
    """
    subextras: Dict[str, Any] = dict()
    if hasattr(cls, "from_settings"):
        from_settings_method = cls.from_settings
    else:
        from_settings_method = cls
    if takes_kwargs(from_settings_method):
        subextras = extras
    else:
        subextras = {
            k: v for k, v in extras.items() if takes_arg(from_settings_method, k)
        }
    return subextras


def __remove_optional(annotation: type) -> type:
    """Optional[X] annotations are actually represented as Union[X, NoneType]."""
    origin = getattr(annotation, "__origin__", None)
    args = getattr(annotation, "__args__", ())

    if origin == Union:
        return Union[tuple([arg for arg in args if arg != type(None)])]
    else:
        return annotation


def __construct_arg(
    class_name: str,
    argument_name: str,
    setting: Any,
    annotation: Type,
    default: Any,
    **extras,
) -> Any:
    """Constructs initializer argument."""
    origin = getattr(annotation, "__origin__", None)
    args = getattr(annotation, "__args__", [])
    # The parameter is optional if its default value is not the "no default" sentinel.
    optional = default != _NO_DEFAULT
    # integer or boolean
    if annotation in {int, bool}:
        if type(setting) in {int, bool}:
            return annotation(setting)
        else:
            raise TypeError(f"Expected {argument_name} to be a {annotation.__name__}.")
    # string
    elif annotation == str:
        if type(setting) == str or isinstance(setting, Path):
            return str(setting)
        else:
            raise TypeError(f"Expected {argument_name} to be a string.")
    # float
    elif annotation == float:
        if type(setting) in {int, float}:
            return setting
        else:
            raise TypeError(f"Expected {argument_name} to be a numeric.")
    # mapping
    elif (
        origin in {collections.abc.Mapping, Mapping, Dict, dict}
        and len(args)
        and can_construct_from_settings(args[-1])
    ):
        value_class = annotation.__args__[-1]
        value_dict = {}
        if not isinstance(setting, Mapping):
            raise TypeError(f"Expected {argument_name} to be a Mapping.")

        for k, v in setting.items():
            value_dict[k] = __construct_arg(
                value_class.__class__.__name__,
                f"{argument_name}.{key}",
                v,
                value_class,
                _NO_DEFAULT,
                **extras,
            )

        return value_dict
    # tuple
    elif origin in (Tuple, tuple) and all(
        __can_construct_from_settings(arg) for arg in args
    ):
        value_list = []

        for i, (value_class, value_setting) in enumerate(
            zip(annotation.__args__, setting)
        ):
            value = __construct_arg(
                value_class.__class__.__name__,
                f"{argument_name}f.{i}",
                value_setting,
                value_class,
                _NO_DEFAULT,
                **extras,
            )

        return tuple(value_list)
    # set
    elif origin in (Set, set) and len(args) == 1 and __can_construct_from_settings(arg):
        value_class = annotation.__args__[0]

        value_set = set()

        for i, value_setting in enumerate(setting):
            value = __construct_arg(
                value_class.__class__.__name__,
                f"{argument_name}f.{i}",
                value_setting,
                value_class,
                _NO_DEFAULT,
                **extras,
            )
            value_set.add(value)

        return value_set

    elif origin == Union:
        _setting = deepcopy(settings)

        error_chain: Optional[Exception] = None
        # at least one of the annotation should be
        # valid for the setting
        for arg in args:
            try:
                __construct_arg(
                    value_class.__class__.__name__,
                    argument_name,
                    setting,
                    arg,
                    _NO_DEFAULT,
                    **extras,
                )
            except (ValueError, TypeError, ConfigurationError, AttributeError):
                # Our attempt to construct the argument may have modified setting, so we
                # restore it here.
                setting = deepcopy(_setting)
                e.args = (f"While constructing an argument of type {arg}",) + e.args
                e.__cause__ = error_chain
                error_chain = e
            # If none of them succeeded, we crash.
            config_error = ConfigurationError(
                f"Failed to construct argument {argument_name} with type {annotation}."
            )
            config_error.__cause__ = error_chain
            raise config_error

    elif (
        origin in {collections.abc.Iterable, Iterable, List, list}
        and len(args) == 1
        and __can_construct_from_settings(args[0])
    ):
        value_class = annotation.__args__[0]

        value_list = []

        for i, value_params in enumerate(setting):
            value = construct_arg(
                str(value_class),
                argument_name + f".{i}",
                value_params,
                value_class,
                _NO_DEFAULT,
                **extras,
            )
            value_list.append(value)

        return value_list

    else:
        return setting


def __pop_and_construct_arg(
    class_name: str,
    argument_name: str,
    annotation: Type,
    default: Any,
    settings: OnclusiveBaseSettings,
    **extras,
) -> Any:
    """Pop and constructs initializer argument."""
    settings_dict = settings.model_dump()
    if argument_name in extras:
        if argument_name not in settings:
            return extras[argument_name]
        else:
            logger.warning(
                f"Setting {argument_name} for class {class_name} was found in both "
                "**extras and in settings object. The extra value will be ignored."
                "This may result in unexpected behaviour."
            )

    popped_setting = (
        settings_dict.pop(argument_name, default)
        if default != _NO_DEFAULT
        else settings_dict.pop(argument_name)
    )
    if popped_setting is None:
        return None

    return __construct_arg(
        class_name, argument_name, popped_setting, annotation, default, **extras
    )


def _create_kwargs(
    constructor: Callable[..., T],
    cls: Type[T],
    settings: OnclusiveBaseSettings,
    **extras,
) -> Dict[str, Any]:
    """Given some class, an `OnclusiveBaseSettings` object, and potentially other
    keyword arguments, create a dict of keyword args suitable for passing to the class's constructor.

    The function does this by finding the class's constructor, matching the constructor
    arguments to entries in the `params` object, and instantiating values for the settings
    using the type annotation and possibly a from_params method.

    Args:
        constructor (Callable[..., T]):
        cls (Type[T]):
        settings (OnclusiveBaseSettings):
    """

    kwargs: Dict[str, Any] = {}

    if constructor is None:
        constructor = cls.__init__
    parameters = __infer_method_signature(cls, constructor)

    accepts_kwargs = False

    for name, parameter in parameters.items():
        if name == "self":
            continue

        if parameter.kind == parameter.VAR_KEYWORD:
            accepts_kwargs = True
            continue

        annotation = __remove_optional(parameter.annotation)
        explicitely_set = name in parameters
        constructed_arg = __pop_and_construct_arg(
            cls.__name__, name, annotation, parameter.default, settings, **extras
        )

        if explicitely_set or constructed_arg is not parameter.default:
            kwargs[name] = constructed_arg

    if accepts_kwargs:
        kwargs.update(parameters)
    return kwargs
