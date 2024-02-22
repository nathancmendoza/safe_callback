"""
    :module_name: context
    :module_summary: capturing of context required by callback guards
    :module_author: Nathan Mendoza
"""


from abc import ABC, abstractmethod
from typing import Iterable, Any, Mapping


class BaseContext(ABC):
    def __init__(self, *args, **kwargs):
        self.positionals = args
        self.keywords = kwargs

    @abstractmethod
    def get_positionals(self) -> Iterable[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_keywords(self) -> Mapping[str, Any]:
        raise NotImplementedError
