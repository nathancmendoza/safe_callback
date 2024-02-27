"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""


class SafeCallback:
    def __init__(self, arg):
        self.args = arg
        self.__f_result = None

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                self.__f_result = func(*args, **kwargs)
            except Exception as err:
                self.f_error(err)
            else:
                self.f_ok()
            finally:
                self.f_finally()

            return self.__f_result
        return wrapper

    def f_error(self, error):
        raise

    def f_ok(self):
        pass

    def f_finally(self):
        pass


"""
class GuardedCallbackBuilder:

    def __init__(self):
        self.__wrapped = _GuardedCallback()

    def set_callback(self, f: Callable[[...], Any]) -> GuardedCallbackBuilder:
        self.__wrapped.protected_callback = f
        return self

    def set_ok_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.__wrapped.ok_callback = f
        return self

    def set_finally_callback(
        self,
        f: Callable[[...], Any]
    ) -> GuardedCallbackBuilder:
        self.__wrapped.cleanup_callback = f
        return self

    def add_context(self, *args, **kwargs) -> GuardedCallbackBuilder:
        self.__wrapped.fargs = args
        self.__wrapped.fkwargs = kwargs
        return self

    def set_dispatcher_class(
        self,
        dispatcher
    ) -> GuardedCallbackBuilder:
        self.__wrapped.dispatcher = dispatcher
        return self

    def set_dispatchable_errors(self, error_map):
        for err, dispatch in error_map.items():
            self.__wrapped.dispatcher.add_dispatchable_error(err, *dispatch)
        return self

    def set_callback_usage(self, usage):
        setattr(
            self.__wrapped,
            "use_callback",
            MethodType(usage, self.__wrapped)
        )

    def set_ok_callback_usage(self, usage):
        setattr(
            self.__wrapped,
            "use_ok_callback",
            MethodType(usage, self.__wrapped)
        )

    def set_finally_callback_ussage(self, usage):
        setattr(
            self.__wrapped,
            "use_final_callback",
            MethodType(usage, self.__wrapped)
        )

    def build_guarded_callback(self):
        return self.__wrapped
"""
