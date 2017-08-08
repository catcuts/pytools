# -*- coding:utf-8 -*-

from functools import wraps


def on_off(s):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if s[func.__name__]:
                return func(*args, **kwargs)
            else:
                return
        return wrapper
    return decorator
