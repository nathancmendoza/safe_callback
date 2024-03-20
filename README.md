# Safe Callback

## About

`safe-callback` is a simple library that provides a way to safely call a function or method and handle anticipated errors in a customizable way. It is designed to be used in situations where a function or method may fail, but the failure is not fatal and should be handled gracefully. However, this situation seems to be common enough that error handling code can become repetitive and clutter the main logic of a program. `safe-callback` aims to simplify this by providing a way to handle errors in a predictable and customizable way.

## Installation

Install `safe-callback` using pip:

```bash
$ pip install safe-callback
```

## Usage

`safe-callback` uses a decorator to wrap a function or method to handle any anticipated errors that may occur in the wrapped function or method. The decorator can specify a mapping of which errors to handle and how to handle them. If an instance of the exception is raised, the corresponding handler will be called. If no handler is specified for a particular exception, the exception will be raised as normal.

### Basic Usage

Use the `@safecallback` decorator to wrap a function or method. Specify the anticipated exceptions and how to handle them as a dictionary.

```python
from safe_callback import safecallback

@safecallback({
  ZeroDivisionError: lambda e: print("Denominator cannot be zero")
})
def divide(numerator, denominator):
  return numerator / denominator
```

In this example, the `divide` function is protected from a `ZeroDivisionError`. If a `ZeroDivisionError` is raised, the provided lambda function is called and the exception is handled. If any other exception is raised, it will be raised as normal.

```python
>>> divide(4, 2) # Returns 2.0 as normal
2.0
>>> divide(4, 0) # Prints "Denominator cannot be zero" and returns None
Denominator cannot be zero
```

### Advanced Usage

The `@safecallback` decorator can also be used without any arguments. In this case, the wrapped function or method will not handle any exceptions, but will allow the exception handlers to be specified at a later time using the `error_handler` sub-decorator. This can be useful when the exception mapping grows too large or for specifying exception handlers at runtime.

```python
@safecallback() # Exception mapping is empty, so no exceptions will be handled
def divide(numerator, denominator):
  return numerator / denominator

# Elsewhere or maybe in some other module
@divide.error_handler(ZeroDivisionError)
def handle_zero_division_error(e):
  print("Denominator cannot be zero")

```
In this example, the `divide` function is initially unprotected. However, the `handle_zero_division_error` function is specified as the exception handler for `ZeroDivisionError` at a later time. This allows the exception handlers to be specified at runtime or in a different module.

```python
>>> divide(4, 2) # Returns 2.0 as normal
2.0
>>> divide(4, 0) # Prints "Denominator cannot be zero" and returns None
Denominator cannot be zero
```
