"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""

from types import MethodType


def safecallback(errors=None):
    def decorator(func):

        def do_error_handling(ctx, error):
            for error_type, handler in ctx.errors.items():
                if isinstance(error, error_type):
                    handler(error)
                    break
            else:
                raise error

        def do_success_handling(ctx):
            pass

        def do_finally_step(ctx):
            pass

        def error_handler(ctx, error_type: Exception):
            def map_error(handler):
                ctx.errors.update({error_type: handler})
            return map_error

        def success_handler(ctx):
            def use_else_workflow(workflow):
                ctx.do_success_handling = MethodType(workflow, ctx)
            return use_else_workflow

        def finally_workflow(ctx):
            def use_finally_workflow(workflow):
                ctx.do_finally_step = MethodType(workflow, ctx)
            return use_finally_workflow

        def wrapper(*args, **kwargs):
            try:
                wrapper.result = func(*args, **kwargs)
            except Exception as err:
                wrapper.do_error_handling(err)
            else:
                wrapper.do_success_handling()
            finally:
                wrapper.do_finally_step()

            return wrapper.result

        wrapper.errors = errors or {}
        wrapper.result = None
        wrapper.do_error_handling = MethodType(do_error_handling, wrapper)
        wrapper.do_success_handling = MethodType(do_success_handling, wrapper)
        wrapper.do_finally_step = MethodType(do_finally_step, wrapper)
        wrapper.error_handler = MethodType(error_handler, wrapper)
        wrapper.success_handler = MethodType(success_handler, wrapper)
        wrapper.finally_workflow = MethodType(finally_workflow, wrapper)
        return wrapper

    return decorator
