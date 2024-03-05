"""
    :module_name: safe_callback
    :module_summary: A declarative approach to exception handling in python
    :module_author: Nathan Mendoza
"""


def safecallback(errors=None):

    class GuardedCallback:
        def __init__(self, func):
            self.__err_map = errors or dict()
            self.__func = func
            self.__f_result = None
            self.__exception = None

        def __call__(self, *args, **kwargs):
            try:
                self.__f_result = self.__func(*args, **kwargs)
            except Exception as err:
                self.__exception = err
                self.__f_error()
            else:
                self.__f_ok()
            finally:
                self.__f_finally()

            return self.__f_result

        def __f_error(self):
            if cb := self.__err_map.get(type(self.__exception)):
                self.__f_result = cb(self.__exception)
            else:
                raise self.__exception

        def __f_ok(self):
            pass

        def __f_finally(self):
            pass

        def error_handler(self, error):
            def error_mapper(f):
                self.__err_map[error] = f
            return error_mapper

    return GuardedCallback
