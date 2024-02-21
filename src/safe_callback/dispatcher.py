"""
    :module_name: dispatch
    :module_summary: Definition of compatible error dispatchers for library interface
    :module_author: Nathan Mendoza
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any, Mapping


class ErrorCallbackDispatcher(ABC):
    def __init__(self, errors: Mapping[Exception, Callable[[...], Any]]):
        self.err_mapping = errors

    @abstractmethod
    def find_error_handler(
        self,
        exc: Exception
    ) -> Callable[[...], Any] | None:
        raise NotImplementedError


class ExactErrorDispatcher(ErrorCallbackDispatcher):
    def find_error_handler(self, exc):
        return self.err_mapping.get(type(exc))


class AbsoluteErrorDispatcher(ErrorCallbackDispatcher):
    def find_error_handler(self, exc):
        for err_type, err_cb in self.err_mapping.items():
            if isinstance(exc, err_type):
                return err_cb
