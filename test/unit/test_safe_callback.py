"""Tests for safe_callback"""
from __future__ import annotations

from unittest.mock import patch
import pytest
import io

import safe_callback


@pytest.fixture
def decorated_function():

    def handle_function_error(e):
        print("Cannot divide because denominator is 0!")

    @safe_callback.safecallback({
        ZeroDivisionError: handle_function_error
    })
    def divide(x, y):
        return x / y

    return divide


@pytest.fixture
def decorated_method():

    def handle_method_error(e):
        print("Cannot divide because denominator is 0!")

    class Calc:

        @safe_callback.safecallback({
            ZeroDivisionError: handle_method_error
        })
        def divide(self, x, y):
            return x / y

    return Calc()


def test_decorated_function_returns_expected_result_on_ok(decorated_function):
    assert decorated_function(4, 2) == 2.0


@patch('sys.stdout', new_callable=io.StringIO)
def test_decorated_function_calls_error_function_on_exception(
    mock_stdout,
    decorated_function
):
    assert decorated_function(4, 0) is None
    expected_output = "Cannot divide because denominator is 0!\n"
    assert mock_stdout.getvalue() == expected_output


def test_decorated_method_returns_expected_result_on_ok(decorated_method):
    assert decorated_method.divide(4, 2) == 2.0


@patch('sys.stdout', new_callable=io.StringIO)
def test_decorated_method_returns_calls_error_function_on_exception(
    mock_stdout,
    decorated_method
):
    assert decorated_method.divide(4, 0) is None
    expected_output = "Cannot divide because denominator is 0!\n"
    assert mock_stdout.getvalue() == expected_output
