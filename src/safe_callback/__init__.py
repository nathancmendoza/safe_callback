"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""


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
            return GuardedCallback(f, errors, *args, **kwargs)()
        return wrapper
    return decorator


class GuardedCallback:
    def __init__(self, f, errors, *fargs, **fkwargs):
        self.f = f
        self.err_dispatch = CallbackErrorDispatch(errors)
        self.f_args = fargs
        self.f_kwargs = fkwargs

    def __call__(self):
        try:
            return self.f(*self.f_args, **self.f_kwargs)
        except Exception as err:
            return self.err_dispatch.on_callback_error(
                err,
                *self.f_args,
                **self.f_kwargs
            )
        else:
            pass
        finally:
            pass


class CallbackErrorDispatch:
    def __init__(self, errors, ok_callback=None, cleanup_callback=None):
        self.err_mapping = errors
        self.on_ok = ok_callback
        self.on_finally = cleanup_callback

    def on_callback_error(self, exception, *args, **kwargs):
        if cb := self.err_mapping.get(type(exception)):
            return cb(exception, *args, **kwargs)
        raise

    def on_callback_ok(self, *args, **kwargs):
        pass

    def on_callback_cleanup(self, *args, **kwargs):
        pass
