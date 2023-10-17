"""This file contains utilities used for the voting rules, such as decorators."""

from preflibtools.instances.preflibinstance import *
from preflibtools.properties.basic import *


class PreferenceIncompatibleError(Exception):
    pass


def requires_preference_type(*dtype):
    def decorator_fn(fn):
        def wrapper_fn(*fn_args, **fn_kw_args):
            if fn_args[0].data_type not in dtype:
                type_str = (("%s, " * (len(dtype) - 1)) + "%s") % dtype
                raise PreferenceIncompatibleError("Only the following types are accepted: %s" % type_str)
            return fn(*fn_args, **fn_kw_args)
        return wrapper_fn
    return decorator_fn


def requires_approval(fn):
    def wrapper_fn(*fn_args, **fn_kw_args):
        if not is_approval(fn_args[0]):
            raise PreferenceIncompatibleError("Only approval preferences are accepted.")
        return fn(*fn_args, **fn_kw_args)
    return wrapper_fn