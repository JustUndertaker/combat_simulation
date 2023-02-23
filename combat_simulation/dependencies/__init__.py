"""
依赖注入容器
"""

import abc
import inspect
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    cast,
)

from pydantic import BaseConfig
from pydantic.fields import FieldInfo, ModelField, Required, Undefined
from pydantic.schema import get_annotation_from_field_info

from ..exception import SkippedException
from ..typing import _DependentCallable
from ..utils import check_field_type, get_typed_signature

R = TypeVar("R")
T = TypeVar("T", bound="Dependent")


class Param(abc.ABC, FieldInfo):
    """依赖注入的基本单元 —— 参数。

    继承自 `pydantic.fields.FieldInfo`，用于描述参数信息（不包括参数名）。
    """

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type["Param"], ...]
    ) -> Optional["Param"]:
        return

    @classmethod
    def _check_parameterless(
        cls, value: Any, allow_types: Tuple[Type["Param"], ...]
    ) -> Optional["Param"]:
        return

    @abc.abstractmethod
    def _solve(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def _check(self, **kwargs: Any) -> None:
        return


class CustomConfig(BaseConfig):
    arbitrary_types_allowed = True


@dataclass(frozen=True)
class Dependent(Generic[R]):
    """依赖注入容器

    参数:
        call: 依赖注入的可调用对象，可以是任何 Callable 对象
        pre_checkers: 依赖注入解析前的参数检查
        params: 具名参数列表
        parameterless: 匿名参数列表
        allow_types: 允许的参数类型
    """

    call: _DependentCallable[R]
    params: Tuple[ModelField] = field(default_factory=tuple)
    parameterless: Tuple[Param] = field(default_factory=tuple)

    def __repr__(self) -> str:
        if inspect.isfunction(self.call) or inspect.isclass(self.call):
            call_str = self.call.__name__
        else:
            call_str = repr(self.call)
        return (
            f"Dependent(call={call_str}"
            + (f", parameterless={self.parameterless}" if self.parameterless else "")
            + ")"
        )

    def __call__(self, **kwargs: Any) -> R:
        # do pre-check
        self.check(**kwargs)

        # solve param values
        values = self.solve(**kwargs)

        return cast(Callable[..., R], self.call)(**values)

    @staticmethod
    def parse_params(
        call: _DependentCallable[R], allow_types: Tuple[Type[Param], ...]
    ) -> Tuple[ModelField]:
        fields: List[ModelField] = []
        params = get_typed_signature(call).parameters.values()

        for param in params:
            default_value = Required
            if param.default != param.empty:
                default_value = param.default

            if isinstance(default_value, Param):
                field_info = default_value
            else:
                for allow_type in allow_types:
                    if field_info := allow_type._check_param(param, allow_types):
                        break
                else:
                    raise ValueError(
                        f"Unknown parameter {param.name} for function {call} with type {param.annotation}"
                    )

            default_value = field_info.default

            annotation: Any = Any
            required = default_value == Required
            if param.annotation != param.empty:
                annotation = param.annotation
            annotation = get_annotation_from_field_info(
                annotation, field_info, param.name
            )

            fields.append(
                ModelField(
                    name=param.name,
                    type_=annotation,
                    class_validators=None,
                    model_config=CustomConfig,
                    default=None if required else default_value,
                    required=required,
                    field_info=field_info,
                )
            )

        return tuple(fields)

    @staticmethod
    def parse_parameterless(
        parameterless: Tuple[Any, ...], allow_types: Tuple[Type[Param], ...]
    ) -> Tuple[Param, ...]:
        parameterless_params: List[Param] = []
        for value in parameterless:
            for allow_type in allow_types:
                if param := allow_type._check_parameterless(value, allow_types):
                    break
            else:
                raise ValueError(f"Unknown parameterless {value}")
            parameterless_params.append(param)
        return tuple(parameterless_params)

    @classmethod
    def parse(
        cls,
        *,
        call: _DependentCallable[R],
        parameterless: Optional[Iterable[Any]] = None,
        allow_types: Iterable[Type[Param]],
    ) -> "Dependent[R]":
        allow_types = tuple(allow_types)

        params = cls.parse_params(call, allow_types)
        parameterless_params = (
            tuple()
            if parameterless is None
            else cls.parse_parameterless(tuple(parameterless), allow_types)
        )

        return cls(call, params, parameterless_params)

    def check(self, **params: Any) -> None:
        try:
            for param in self.parameterless:
                param._check(**params)
            for param in self.params:
                cast(Param, param.field_info)._check(**params)

        except SkippedException:
            # logger.trace(f"{self} skipped due to {e}")
            raise

    def _solve_field(self, field: ModelField, params: Dict[str, Any]) -> Any:
        value = cast(Param, field.field_info)._solve(**params)
        if value is Undefined:
            value = field.get_default()
        return check_field_type(field, value)

    def solve(self, **params: Any) -> Dict[str, Any]:
        # solve parameterless
        for param in self.parameterless:
            param._solve(**params)

        # solve param values
        values = []
        for _field in self.params:
            values.append(self._solve_field(_field, params))

        return {field.name: value for field, value in zip(self.params, values)}
