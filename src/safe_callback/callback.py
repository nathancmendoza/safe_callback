"""
    :module_name: callback
    :module_summary: Definition of compatible callbacks for library interface
    :module_author: Nathan Mendoza
"""

from __future__ import annotations
from typing import Callable, Any, Tuple, Dict, Type
from .dispatcher import ErrorCallbackDispatcher


class _GuardedCallback:
    def __init__(self):
        self.__f = None
        self.__f_ok = None
        self.__f_finally = None
        self.__err_dispatch = None
        self.__f_args = None
        self.__f_kwargs = None
        self.__f_result = None

    def __call__(self):
        try:
            self.use_callback()
        except Exception as err:
            self.use_error_callback(
                self.err_dispatch.find_error_handler(err),
                err
            )
        else:
            self.use_ok_callback()
        finally:
            self.use_final_callback()

        return self.fresult

    @property
    def protected_callback(self):
        """The protected_callback property."""
        return self.__f

    @protected_callback.setter
    def protected_callback(self, cb: Callable[[...], Any]):
        self.__f = cb

    @property
    def ok_callback(self):
        """The ok_callback property."""
        return self.__f_ok

    @ok_callback.setter
    def ok_callback(self, cb: Callable[[...], Any]):
        self.__f_ok = cb

    @property
    def cleanup_callback(self):
        """The cleanup_callback property."""
        return self.__f_finally

    @cleanup_callback.setter
    def cleanup_callback(self, cb: Callable[[...], Any]):
        self.__f_finally = cb

    @property
    def fargs(self):
        """The fargs property."""
        return self.__f_args

    @fargs.setter
    def fargs(self, arguments: Tuple[Any]):
        self.__f_args = arguments

    @property
    def fkwargs(self):
        """The fkwargs property."""
        return self.__f_kwargs

    @fkwargs.setter
    def fkwargs(self, keyword_arguments: Dict[str, Any]):
        self.__f_kwargs = keyword_arguments

    @property
    def fresult(self):
        """The fresult property."""
        return self.__f_result

    @fresult.setter
    def fresult(self, value: Any):
        self.__f_result = value

    @property
    def dispatcher(self):
        """The dispatcher property."""
        return self.__err_dispatch

    @dispatcher.setter
    def dispatcher(self, dispatcher_class: Type[ErrorCallbackDispatcher]):
        self.__err_dispatch = dispatcher_class()

    def use_callback(self):
        self.fresult = self.__f(*self.fargs, **self.fkwargs)

    def use_ok_callback(self):
        pass

    def use_final_callback(self):
        pass
