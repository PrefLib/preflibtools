"""This file contains decorators which can be used in other functions to ensure
the input instance type is supported by the function."""

from functools import wraps
from preflibtools.properties.basic import is_approval


class PreferenceIncompatibleError(Exception):
    """Exception raised if an instance with a different type of preferences than expected was encountered."""

    pass


def requires_preference_type(*dtype):
    """Decorator to filter instances with wrong preference type."""

    def decorator_fn(fn):
        @wraps(fn)
        def wrapper_fn(*fn_args, **fn_kw_args):
            if fn_args[0].data_type not in dtype:
                type_str = (("%s, " * (len(dtype) - 1)) + "%s") % dtype
                raise PreferenceIncompatibleError(
                    "Only the following types are accepted: %s" % type_str
                )
            return fn(*fn_args, **fn_kw_args)

        return wrapper_fn

    return decorator_fn


def requires_approval(fn):
    """Decorator to filter ordinal instances that are not approval."""

    @wraps(fn)
    def wrapper_fn(*fn_args, **fn_kw_args):
        if not is_approval(fn_args[0]):
            raise PreferenceIncompatibleError("Only approval preferences are accepted.")
        return fn(*fn_args, **fn_kw_args)

    return wrapper_fn
