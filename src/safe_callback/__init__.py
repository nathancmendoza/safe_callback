"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""

from __future__ import annotations
from typing import Callable, Any
from types import MethodType

from .callback import _GuardedCallback
from .dispatcher import AbsoluteErrorDispatcher


def safecallback(
    errors,
    # callback_ok,
    # callback_cleanup,
    # pass_context,
    # follow_exc_hierarchies,
    # reraise_unknown
):
    def decorator(f):
        def wrapper(*args, **kwargs):
            return GuardedCallbackBuilder() \
                .set_callback(f) \
                .set_dispatcher_class(AbsoluteErrorDispatcher) \
                .set_dispatchable_errors(errors) \
                .add_context(*args, **kwargs) \
                .set_ok_callback(None) \
                .set_finally_callback(None) \
                .build_guarded_callback()()
        return wrapper
    return decorator


class GuardedCallbackBuilder:

    def __init__(self):
        self.__wrapped = _GuardedCallback()

    def set_callback(self, f: Callable[[...], Any]) -> GuardedCallbackBuilder:
        self.__wrapped.protected_callback = f
        return self

    def set_ok_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.__wrapped.ok_callback = f
        return self

    def set_finally_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.__wrapped.cleanup_callback = f
        return self

    def add_context(self, *args, **kwargs) -> GuardedCallbackBuilder:
        self.__wrapped.fargs = args
        self.__wrapped.fkwargs = kwargs
        return self

    def set_dispatcher_class(
        self,
        dispatcher
    ) -> GuardedCallbackBuilder:
        self.__wrapped.dispatcher = dispatcher
        return self

    def set_dispatchable_errors(self, error_map):
        for err, dispatch in error_map.items():
            self.__wrapped.dispatcher.add_dispatchable_error(err, *dispatch)
        return self

    def set_callback_usage(self, usage):
        setattr(
            self.__wrapped,
            "use_callback",
            MethodType(usage, self.__wrapped)
        )

    def set_ok_callback_usage(self, usage):
        setattr(
            self.__wrapped,
            "use_ok_callback",
            MethodType(usage, self.__wrapped)
        )

    def set_finally_callback_ussage(self, usage):
        setattr(
            self.__wrapped,
            "use_final_callback",
            MethodType(usage, self.__wrapped)
        )

    def build_guarded_callback(self):
        return self.__wrapped
