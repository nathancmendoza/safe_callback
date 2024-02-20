"""Tests for safe_callback"""
from __future__ import annotations

import pytest

import safe_callback


@pytest.fixture
def decorated_function():

    def handle_function_error(e, x, y):
        return f"Cannot divide {x} and {y} because denominator is 0!"

    @safe_callback.safecallback({
        ZeroDivisionError: handle_function_error
    })
    def divide(x, y):
        return x / y

    return divide


@pytest.fixture
def decorated_method():

    def handle_method_error(self, e, x, y):
        return f"Cannot divide {x} and {y} because denominator is 0!"

    class Calc:

        @safe_callback.safecallback({
            ZeroDivisionError: handle_method_error
        })
        def divide(self, x, y):
            return x / y

    return Calc()


def test_decorated_function_returns_expected_result_on_ok(decorated_function):
    assert decorated_function(4, 2) == 2.0


def test_decorated_function_calls_error_function_on_exception(
    decorated_function
):
    assert decorated_function(
        4, 0) == "Cannot divide 4 and 0 because denominator is 0!"


def test_decorated_method_returns_expected_result_on_ok(decorated_method):
    assert decorated_method.divide(4, 2) == 2.0


def test_decorated_method_returns_calls_error_function_on_exception(
    decorated_method
):
    assert decorated_method.divide(
        4, 0) == "Cannot divide 4 and 0 because denominator is 0!"
