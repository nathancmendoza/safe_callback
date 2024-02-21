"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""

from .callback import GuardedCallbackBuilder
from .dispatcher import AbsoluteErrorDispatcher


def safecallback(
    errors,
    # callback_ok,
    # callback_cleanup,
    # pass_context,
    # follow_exc_hierarchies,
    # reraise_unknown
):
    def decorator(f):
        def wrapper(*args, **kwargs):
            return GuardedCallbackBuilder() \
                .set_callback(f) \
                .set_dispatcher_class(AbsoluteErrorDispatcher) \
                .set_pass_context(True) \
                .add_context(*args, **kwargs) \
                .set_ok_callback(None) \
                .set_finally_callback(None) \
                .build_guarded_callback(errors)()
        return wrapper
    return decorator
