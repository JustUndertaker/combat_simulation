"""
定义异常
"""
from typing import Any

from pydantic.fields import ModelField


class BaseException(Exception):
    """基础异常"""

    def __str__(self) -> str:
        return self.__repr__()


class SkippedException(BaseException):
    """立即结束当前 `Dependent` 的运行。"""


class TypeMisMatch(SkippedException):
    """当前 `Handler` 的参数类型不匹配。"""

    def __init__(self, param: ModelField, value: Any):
        self.param: ModelField = param
        self.value: Any = value

    def __repr__(self) -> str:
        return (
            f"TypeMisMatch(param={self.param.name}, "
            f"type={self.param._type_display()}, value={self.value!r}>"
        )
