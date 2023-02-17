"""
定义typing
"""
from typing import Callable, TypeVar

T = TypeVar("T")

_DependentCallable = Callable[..., T]
