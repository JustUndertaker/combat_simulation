"""
定义typing
"""
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")

_DependentCallable = Callable[..., T]

T_State = Dict[Any, Any]
"""事件处理状态 State 类型"""
T_Handler = _DependentCallable[Any]
"""Handler 处理函数。"""
T_DependencyCache = Dict[_DependentCallable[Any], Any]
"""依赖缓存, 用于存储依赖函数的返回值"""
