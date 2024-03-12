"""Tests for safe_callback"""
from __future__ import annotations

from unittest.mock import patch
import pytest
import io

import safe_callback


@pytest.fixture
def generic_error_handler():
    def log_error(e):
        print(f"Error: {e}")

    return log_error


@pytest.fixture
def error_prone_function(generic_error_handler):
    @safe_callback.safecallback({
        ZeroDivisionError: generic_error_handler
    })
    def do_something_that_might_fail(
        identity,
        raise_an_exception=False,
        exception_to_raise=Exception
    ):
        if raise_an_exception:
            raise exception_to_raise("This is an exception")
        return identity

    return do_something_that_might_fail


@pytest.fixture
def class_with_error_prone_methods(generic_error_handler):

    class Calculator:

        @safe_callback.safecallback({
            ZeroDivisionError: generic_error_handler
        })
        def do_something_that_might_fail(
            self,
            identity,
            raise_an_exception=False,
            exception_to_raise=Exception
        ):
            if raise_an_exception:
                raise exception_to_raise("This is an exception")
            return identity

        @safe_callback.safecallback({
            ZeroDivisionError: generic_error_handler
        })
        @staticmethod
        def do_something_that_might_fail_statically(
            identity,
            raise_an_exception=False,
            exception_to_raise=Exception
        ):
            if raise_an_exception:
                raise exception_to_raise("This is an exception")
            return identity

        @safe_callback.safecallback({
            ZeroDivisionError: generic_error_handler
        })
        @classmethod
        def create_instance_that_might_fail(
            cls,
            raise_an_exception=False,
            exception_to_raise=Exception
        ):
            if raise_an_exception:
                raise exception_to_raise("This is an exception")
            return cls()

    return Calculator


@pytest.fixture
def decorated_bounded_method(class_with_error_prone_methods):
    return class_with_error_prone_methods().do_something_that_might_fail


@pytest.fixture
def decorated_static_method(class_with_error_prone_methods):
    return class_with_error_prone_methods.divide_static


@pytest.fixture
def decorated_class_method(class_with_error_prone_methods):
    return class_with_error_prone_methods.divide_class


def test_decorator_applies_required_attributes_to_function(error_prone_function):
    divide = error_prone_function

    assert hasattr(divide, 'errors')
    assert hasattr(divide, 'result')
    assert hasattr(divide, 'do_error_handling')
    assert hasattr(divide, 'do_success_handling')
    assert hasattr(divide, 'do_finally_step')
    assert hasattr(divide, 'error_handler')
    assert hasattr(divide, 'success_handler')
    assert hasattr(divide, 'finally_workflow')


def test_decorator_applies_required_attributes_to_method(decorated_bounded_method):
    calc = decorated_bounded_method

    assert hasattr(calc, 'errors')
    assert hasattr(calc, 'result')
    assert hasattr(calc, 'do_error_handling')
    assert hasattr(calc, 'do_success_handling')
    assert hasattr(calc, 'do_finally_step')
    assert hasattr(calc, 'error_handler')
    assert hasattr(calc, 'success_handler')
    assert hasattr(calc, 'finally_workflow')


class TestDecoratedFunctionUsage:
    @pytest.mark.parametrize(
        "value", range(1, 10)
    )
    def test_decorated_function_returns_result_on_success(
        self,
        value,
        error_prone_function
    ):
        assert error_prone_function(value) == value

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_decorated_function_calls_error_handler_on_mapped_exception(
        self,
        mock_stdout,
        error_prone_function
    ):
        assert error_prone_function(
            1,
            raise_an_exception=True,
            exception_to_raise=ZeroDivisionError
        ) is None
        assert mock_stdout.getvalue() == "Error: This is an exception\n"

    @pytest.mark.parametrize(
        "exc", [TypeError, ValueError]
    )
    def test_decorated_function_raises_exception_on_unmapped_exception(
        self,
        exc,
        error_prone_function
    ):
        with pytest.raises(exc):
            error_prone_function(
                1,
                raise_an_exception=True,
                exception_to_raise=exc
            )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mapping_additional_exception_after_decorated_function_declaration(
        self,
        mock_stdout,
        error_prone_function,
        generic_error_handler
    ):

        with pytest.raises(FileNotFoundError):
            error_prone_function(
                1,
                raise_an_exception=True,
                exception_to_raise=FileNotFoundError
            )

        @error_prone_function.error_handler(FileNotFoundError)
        def handle_file_not_found(e):
            print("File not found. Exiting...")

        assert error_prone_function(
            1,
            raise_an_exception=True,
            exception_to_raise=FileNotFoundError
        ) is None
        assert mock_stdout.getvalue() == "File not found. Exiting...\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_success_handler_on_decorated_function(
        self,
        mock_stdout,
        error_prone_function
    ):
        assert error_prone_function(1) == 1
        assert mock_stdout.getvalue() == ""

        @error_prone_function.success_handler()
        def handle_success(ctx):
            print("The functional operation succeeded!")

        assert error_prone_function(1) == 1
        assert mock_stdout.getvalue() == "The functional operation succeeded!\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_final_workflow_on_decorated_function(
        self,
        mock_stdout,
        error_prone_function
    ):
        assert error_prone_function(1) == 1
        assert mock_stdout.getvalue() == ""

        @error_prone_function.finally_workflow()
        def cleanup(ctx):
            print("Concluding functional operation")

        assert error_prone_function(1) == 1
        assert mock_stdout.getvalue() == "Concluding functional operation\n"
