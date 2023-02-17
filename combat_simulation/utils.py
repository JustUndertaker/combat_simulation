"""
定义工具
"""
import inspect
from typing import Any, Callable, Dict, ForwardRef, TypeVar

from loguru import logger
from pydantic.fields import ModelField
from pydantic.typing import evaluate_forwardref

from .exception import TypeMisMatch

T = TypeVar("T")
V = TypeVar("V")
T_Wrapped = TypeVar("T_Wrapped", bound=Callable)


def overrides(InterfaceClass: object) -> Callable[[T_Wrapped], T_Wrapped]:
    """标记一个方法为父类 interface 的 implement"""

    def overrider(func: T_Wrapped) -> T_Wrapped:
        assert func.__name__ in dir(InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """获取可调用对象签名"""
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    """获取参数的类型注解"""
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        try:
            annotation = evaluate_forwardref(annotation, globalns, globalns)
        except Exception as e:
            logger.opt(colors=True, exception=e).warning(
                f'Unknown ForwardRef["{param.annotation}"] for parameter {param.name}'
            )
            return inspect.Parameter.empty
    return annotation


def check_field_type(field: ModelField, value: V) -> V:
    _, errs_ = field.validate(value, {}, loc=())
    if errs_:
        raise TypeMisMatch(field, value)
    return value
