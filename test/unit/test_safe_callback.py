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

        @staticmethod
        @safe_callback.safecallback({
            ZeroDivisionError: generic_error_handler
        })
        def do_something_that_might_fail_statically(
            identity,
            raise_an_exception=False,
            exception_to_raise=Exception
        ):
            if raise_an_exception:
                raise exception_to_raise("This is an exception")
            return identity

        @classmethod
        @safe_callback.safecallback({
            ZeroDivisionError: generic_error_handler
        })
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
    return class_with_error_prone_methods.do_something_that_might_fail_statically


@pytest.fixture
def decorated_class_method(class_with_error_prone_methods):
    return class_with_error_prone_methods.create_instance_that_might_fail


def test_decorator_applies_required_attributes_to_function(error_prone_function):
    f = error_prone_function

    assert hasattr(f, 'errors')
    assert hasattr(f, 'result')
    assert hasattr(f, 'do_error_handling')
    assert hasattr(f, 'do_success_handling')
    assert hasattr(f, 'do_finally_step')
    assert hasattr(f, 'error_handler')
    assert hasattr(f, 'success_handler')
    assert hasattr(f, 'finally_workflow')


def test_decorator_applies_required_attributes_to_method(decorated_bounded_method):
    m = decorated_bounded_method

    assert hasattr(m, 'errors')
    assert hasattr(m, 'result')
    assert hasattr(m, 'do_error_handling')
    assert hasattr(m, 'do_success_handling')
    assert hasattr(m, 'do_finally_step')
    assert hasattr(m, 'error_handler')
    assert hasattr(m, 'success_handler')
    assert hasattr(m, 'finally_workflow')


def test_decorator_applies_required_attributes_to_staticmethod(decorated_static_method):
    m = decorated_static_method

    assert hasattr(m, 'errors')
    assert hasattr(m, 'result')
    assert hasattr(m, 'do_error_handling')
    assert hasattr(m, 'do_success_handling')
    assert hasattr(m, 'do_finally_step')
    assert hasattr(m, 'error_handler')
    assert hasattr(m, 'success_handler')
    assert hasattr(m, 'finally_workflow')


def test_decorator_applies_required_attributes_to_classmethod(decorated_class_method):
    m = decorated_class_method

    assert hasattr(m, 'errors')
    assert hasattr(m, 'result')
    assert hasattr(m, 'do_error_handling')
    assert hasattr(m, 'do_success_handling')
    assert hasattr(m, 'do_finally_step')
    assert hasattr(m, 'error_handler')
    assert hasattr(m, 'success_handler')
    assert hasattr(m, 'finally_workflow')


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


class TestDecoratedInstanceMethodUsage:
    @pytest.mark.parametrize(
        "value", range(1, 10)
    )
    def test_decorated_instance_method_returns_result_on_success(
        self,
        value,
        decorated_bounded_method
    ):
        assert decorated_bounded_method(value) == value

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_decorated_instance_method_calls_error_handler_on_mapped_exception(
        self,
        mock_stdout,
        decorated_bounded_method
    ):
        assert decorated_bounded_method(
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
        decorated_bounded_method
    ):
        with pytest.raises(exc):
            decorated_bounded_method(
                1,
                raise_an_exception=True,
                exception_to_raise=exc
            )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mapping_additional_exception_after_decorated_instance_method_declaration(
        self,
        mock_stdout,
        decorated_bounded_method,
        generic_error_handler
    ):

        with pytest.raises(FileNotFoundError):
            decorated_bounded_method(
                1,
                raise_an_exception=True,
                exception_to_raise=FileNotFoundError
            )

        @decorated_bounded_method.error_handler(FileNotFoundError)
        def handle_file_not_found(e):
            print("File not found. Exiting...")

        assert decorated_bounded_method(
            1,
            raise_an_exception=True,
            exception_to_raise=FileNotFoundError
        ) is None
        assert mock_stdout.getvalue() == "File not found. Exiting...\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_success_handler_on_decorated_instance_method(
        self,
        mock_stdout,
        decorated_bounded_method
    ):
        assert decorated_bounded_method(1) == 1
        assert mock_stdout.getvalue() == ""

        @decorated_bounded_method.success_handler()
        def handle_success(ctx):
            print("The bounded operation succeeded!")

        assert decorated_bounded_method(1) == 1
        assert mock_stdout.getvalue() == "The bounded operation succeeded!\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_final_workflow_on_decorated_instance_method(
        self,
        mock_stdout,
        decorated_bounded_method
    ):
        assert decorated_bounded_method(1) == 1
        assert mock_stdout.getvalue() == ""

        @decorated_bounded_method.finally_workflow()
        def cleanup(ctx):
            print("Concluding bounded operation")

        assert decorated_bounded_method(1) == 1
        assert mock_stdout.getvalue() == "Concluding bounded operation\n"


class TestDecoratedStaticMethodUsage:
    @pytest.mark.parametrize(
        "value", range(1, 10)
    )
    def test_decorated_static_method_returns_result_on_success(
        self,
        value,
        decorated_static_method
    ):
        assert decorated_static_method(value) == value

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_decorated_static_method_calls_error_handler_on_mapped_exception(
        self,
        mock_stdout,
        decorated_static_method
    ):
        assert decorated_static_method(
            1,
            raise_an_exception=True,
            exception_to_raise=ZeroDivisionError
        ) is None
        assert mock_stdout.getvalue() == "Error: This is an exception\n"

    @pytest.mark.parametrize(
        "exc", [TypeError, ValueError]
    )
    def test_decorated_static_method_raises_exception_on_unmapped_exception(
        self,
        exc,
        decorated_static_method
    ):
        with pytest.raises(exc):
            decorated_static_method(
                1,
                raise_an_exception=True,
                exception_to_raise=exc
            )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mapping_additional_exception_after_decorated_static_method_declaration(
        self,
        mock_stdout,
        decorated_static_method,
        generic_error_handler
    ):

        with pytest.raises(FileNotFoundError):
            decorated_static_method(
                1,
                raise_an_exception=True,
                exception_to_raise=FileNotFoundError
            )

        @decorated_static_method.error_handler(FileNotFoundError)
        def handle_file_not_found(e):
            print("File not found. Exiting...")

        assert decorated_static_method(
            1,
            raise_an_exception=True,
            exception_to_raise=FileNotFoundError
        ) is None
        assert mock_stdout.getvalue() == "File not found. Exiting...\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_success_handler_on_decorated_static_method(
        self,
        mock_stdout,
        decorated_static_method
    ):
        assert decorated_static_method(1) == 1
        assert mock_stdout.getvalue() == ""

        @decorated_static_method.success_handler()
        def handle_success(ctx):
            print("The staticmethod operation succeeded!")

        assert decorated_static_method(1) == 1
        assert mock_stdout.getvalue() == "The staticmethod operation succeeded!\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_final_workflow_on_decorated_static_method(
        self,
        mock_stdout,
        decorated_static_method
    ):
        assert decorated_static_method(1) == 1
        assert mock_stdout.getvalue() == ""

        @decorated_static_method.finally_workflow()
        def cleanup(ctx):
            print("Concluding staticmethod operation")

        assert decorated_static_method(1) == 1
        assert mock_stdout.getvalue() == "Concluding staticmethod operation\n"


class TestDecoratedClassMethodUsage:
    def test_decorated_class_method_returns_result_on_success(
        self,
        decorated_class_method,
        class_with_error_prone_methods
    ):
        assert isinstance(decorated_class_method(),
                          class_with_error_prone_methods)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_decorated_class_method_calls_error_handler_on_mapped_exception(
        self,
        mock_stdout,
        decorated_class_method
    ):
        assert decorated_class_method(
            raise_an_exception=True,
            exception_to_raise=ZeroDivisionError
        ) is None
        assert mock_stdout.getvalue() == "Error: This is an exception\n"

    @pytest.mark.parametrize(
        "exc", [TypeError, ValueError]
    )
    def test_decorated_class_method_raises_exception_on_unmapped_exception(
        self,
        exc,
        decorated_class_method
    ):
        with pytest.raises(exc):
            decorated_class_method(
                raise_an_exception=True,
                exception_to_raise=exc
            )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mapping_additional_exception_after_decorated_class_method_declaration(
        self,
        mock_stdout,
        decorated_class_method,
        generic_error_handler
    ):

        with pytest.raises(FileNotFoundError):
            decorated_class_method(
                raise_an_exception=True,
                exception_to_raise=FileNotFoundError
            )

        @decorated_class_method.error_handler(FileNotFoundError)
        def handle_file_not_found(e):
            print("File not found. Exiting...")

        assert decorated_class_method(
            raise_an_exception=True,
            exception_to_raise=FileNotFoundError
        ) is None
        assert mock_stdout.getvalue() == "File not found. Exiting...\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_success_handler_on_decorated_class_method(
        self,
        mock_stdout,
        decorated_class_method,
        class_with_error_prone_methods
    ):
        assert isinstance(decorated_class_method(),
                          class_with_error_prone_methods)
        assert mock_stdout.getvalue() == ""

        @decorated_class_method.success_handler()
        def handle_success(ctx):
            print("The staticmethod operation succeeded!")

        assert isinstance(decorated_class_method(),
                          class_with_error_prone_methods)
        assert mock_stdout.getvalue() == "The staticmethod operation succeeded!\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_custom_final_workflow_on_decorated_class_method(
        self,
        mock_stdout,
        decorated_class_method,
        class_with_error_prone_methods
    ):
        assert isinstance(decorated_class_method(),
                          class_with_error_prone_methods)
        assert mock_stdout.getvalue() == ""

        @decorated_class_method.finally_workflow()
        def cleanup(ctx):
            print("Concluding staticmethod operation")

        assert isinstance(decorated_class_method(),
                          class_with_error_prone_methods)
        assert mock_stdout.getvalue() == "Concluding staticmethod operation\n"
