"""Tests for the context submodules"""

import pytest

from safe_callback.context import BaseContext


def test_base_context_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseContext()
