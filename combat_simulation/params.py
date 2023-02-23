import inspect
from contextlib import ExitStack, contextmanager
from typing import Any, Callable, Optional, Tuple, Type, cast

from pydantic.fields import Required, Undefined

from .dependencies import Dependent, Param
from .typing import T_DependencyCache, T_Handler, T_State
from .utils import get_name, is_gen_callable


class DependsInner:
    def __init__(
        self,
        dependency: Optional[T_Handler] = None,
        *,
        use_cache: bool = True,
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache

    def __repr__(self) -> str:
        dep = get_name(self.dependency)
        cache = "" if self.use_cache else ", use_cache=False"
        return f"DependsInner({dep}{cache})"


def Depends(
    dependency: Optional[T_Handler] = None,
    *,
    use_cache: bool = True,
) -> Any:
    """子依赖装饰器

    参数:
        dependency: 依赖函数。默认为参数的类型注释。
        use_cache: 是否使用缓存。默认为 `True`。

    用法:
        ```python
        def depend_func() -> Any:
            return ...

        def depend_gen_func():
            try:
                yield ...
            finally:
                ...

        async def handler(param_name: Any = Depends(depend_func), gen: Any = Depends(depend_gen_func)):
            ...
        ```
    """
    return DependsInner(dependency, use_cache=use_cache)


class DependParam(Param):
    """子依赖参数"""

    def __repr__(self) -> str:
        return f"Depends({self.extra['dependent']})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["DependParam"]:
        if isinstance(param.default, DependsInner):
            dependency: T_Handler
            if param.default.dependency is None:
                assert param.annotation is not param.empty, "Dependency cannot be empty"
                dependency = param.annotation
            else:
                dependency = param.default.dependency
            sub_dependent = Dependent[Any].parse(
                call=dependency,
                allow_types=allow_types,
            )
            return cls(
                Required, use_cache=param.default.use_cache, dependent=sub_dependent
            )

    @classmethod
    def _check_parameterless(
        cls, value: Any, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["Param"]:
        if isinstance(value, DependsInner):
            assert value.dependency, "Dependency cannot be empty"
            dependent = Dependent[Any].parse(
                call=value.dependency, allow_types=allow_types
            )
            return cls(Required, use_cache=value.use_cache, dependent=dependent)

    def _solve(
        self,
        stack: Optional[ExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
        **kwargs: Any,
    ) -> Any:
        use_cache: bool = self.extra["use_cache"]
        dependency_cache = {} if dependency_cache is None else dependency_cache

        sub_dependent: Dependent = self.extra["dependent"]
        call = cast(Callable[..., Any], sub_dependent.call)

        # solve sub dependency with current cache
        sub_values = sub_dependent.solve(
            stack=stack,
            dependency_cache=dependency_cache,
            **kwargs,
        )

        # run dependency function
        task: Any
        if use_cache and call in dependency_cache:
            return dependency_cache[call]
        elif is_gen_callable(call):
            assert isinstance(
                stack, ExitStack
            ), "Generator dependency should be called in context"
            cm = contextmanager(call)(**sub_values)
            task = stack.enter_context(cm)
            dependency_cache[call] = task
            return task
        else:
            task = call(**sub_values)
            dependency_cache[call] = task
            return task

    def _check(self, **kwargs: Any) -> None:
        # run sub dependent pre-checkers
        sub_dependent: Dependent = self.extra["dependent"]
        sub_dependent.check(**kwargs)


class StateParam(Param):
    """事件处理状态参数"""

    def __repr__(self) -> str:
        return "StateParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["StateParam"]:
        if param.default == param.empty:
            if param.annotation is T_State:
                return cls(Required)
            elif param.annotation == param.empty and param.name == "state":
                return cls(Required)

    def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class DefaultParam(Param):
    """默认值参数"""

    def __repr__(self) -> str:
        return f"DefaultParam(default={self.default!r})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["DefaultParam"]:
        if param.default != param.empty:
            return cls(param.default)

    async def _solve(self, **kwargs: Any) -> Any:
        return Undefined
