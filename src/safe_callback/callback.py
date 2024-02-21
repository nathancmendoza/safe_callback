"""
    :module_name: callback
    :module_summary: Definition of compatible callbacks for library interface
    :module_author: Nathan Mendoza
"""

from __future__ import annotations
from typing import Callable, Any
from abc import ABC, abstractmethod


class GuardedCallback(ABC):
    def __init__(
        self,
        f,
        error_dispatcher,
        errors,
        f_ok,
        f_finally,
        *fargs,
        **fkwargs
    ):
        self.f = f
        self.err_dispatch = error_dispatcher(errors)
        self.f_args = fargs
        self.f_kwargs = fkwargs
        self.callback_result = None

    def __call__(self):
        try:
            self._use_callback()
        except Exception as err:
            self._use_error_callback(
                self.err_dispatch.find_error_handler(err),
                err
            )
        else:
            self._use_ok_callback()
        finally:
            self._use_final_callback()

        return self.callback_result

    @abstractmethod
    def _use_callback(self):
        raise NotImplementedError

    @abstractmethod
    def _use_error_callback(
        self,
        cb: Callable[[Exception, ...], Any],
        error: Exception
    ):
        raise NotImplementedError

    @abstractmethod
    def _use_ok_callback(self):
        raise NotImplementedError

    @abstractmethod
    def _use_final_callback(self):
        raise NotImplementedError


class BasicGuardedCallback(GuardedCallback):
    def _use_callback(self):
        self.callback_result = self.f(*self.f_args, **self.f_kwargs)

    def _use_error_callback(self, cb, error):
        if cb:
            self.callback_result = cb(error, *self.f_args, **self.f_kwargs)
        else:
            raise

    def _use_ok_callback(self):
        pass

    def _use_final_callback(self):
        pass


class GuardedCallbackBuilder:
    def set_callback(self, f: Callable[[...], Any]) -> GuardedCallbackBuilder:
        self.f = f
        return self

    def set_ok_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.ok_callback = f
        return self

    def set_finally_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.finally_callback = f
        return self

    def set_pass_context(self, yes: bool) -> GuardedCallbackBuilder:
        self.pass_context = yes
        return self

    def add_context(self, *args, **kwargs) -> GuardedCallbackBuilder:
        self.f_args = args
        self.f_kwargs = kwargs
        return self

    def set_error_interpretation_behavior(
        self,
        behavior
    ) -> GuardedCallbackBuilder:
        self.error_interpretation = behavior
        return self

    def set_dispatcher_class(
        self,
        dispatcher
    ) -> GuardedCallbackBuilder:
        self.dispatcher = dispatcher
        return self

    def build_guarded_callback(self, errors):
        return BasicGuardedCallback(
            self.f,
            self.dispatcher,
            errors,
            self.ok_callback,
            self.finally_callback,
            *self.f_args,
            **self.f_kwargs
        )
