"""
    :module_name: dispatch
    :module_summary: Definition of compatible error dispatchers for library interface
    :module_author: Nathan Mendoza
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any, Type, Optional
from dataclasses import dataclass


@dataclass
class ErrorCallback:
    handler: Callable[[...], Any]
    usage: Optional[Callable[[...], Any]]


class ErrorCallbackDispatcher(ABC):
    def __init__(self):
        self.err_mapping = {}

    @abstractmethod
    def dispatch_error(
        self,
        exc: Exception
    ) -> ErrorCallback | None:
        raise NotImplementedError

    def add_dispatchable_error(
        self,
        exc: Type[Exception],
        handler: Callable[[...], Any],
        usage: Optional[Callable[[...], Any]] = None
    ) -> None:
        self.err_mapping.update({exc: ErrorCallback(handler, usage)})


class ExactErrorDispatcher(ErrorCallbackDispatcher):
    def dispatch_error(self, exc):
        return self.err_mapping.get(type(exc))


class AbsoluteErrorDispatcher(ErrorCallbackDispatcher):
    def dispatch_error(self, exc):
        for err_type, err_cb in self.err_mapping.items():
            if isinstance(exc, err_type):
                return err_cb
