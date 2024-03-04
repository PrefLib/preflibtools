"""This file contains decorators which can be used in other functions to ensure
the input instance type is supported by the function."""

from functools import wraps


class PreferenceIncompatibleError(Exception):
    """Exception raised if an instance with a different type of preferences than expected was encountered."""

    pass


def requires_preference_type(*dtype):
    """Decorator to filter instances with wrong preference type."""

    def decorator_fn(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            if instance.data_type not in dtype:
                raise PreferenceIncompatibleError(
                    f"The function {func.__name__} requires instances with one of the following "
                    f"type: {','.join(dtype)}. The current instance has type {instance.data_type}, "
                    f"which is not allowed.")
            return func(instance, *args, **kwargs)
        return wrapper
    return decorator_fn


def requires_approval(fn):
    """Decorator to filter ordinal instances that are not approval."""
    from preflibtools.properties.basic import is_approval

    @wraps(fn)
    def wrapper_fn(*fn_args, **fn_kw_args):
        if not is_approval(fn_args[0]):
            raise PreferenceIncompatibleError("Only approval preferences are accepted.")
        return fn(*fn_args, **fn_kw_args)

    return wrapper_fn
