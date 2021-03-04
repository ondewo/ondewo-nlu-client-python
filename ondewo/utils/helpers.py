import functools
from typing import Dict, Any

from google.protobuf.struct_pb2 import Struct


def get_struct_from_dict(d: Dict) -> Struct:  # type: ignore
    """
    create  a protobuf Struct from some dict
    Args:
        d (Dict):

    Returns:

    """
    assert (isinstance(d, dict) or d is None), 'parameter must be a dict or None'

    result: Struct = Struct()  # type: ignore

    if d is not None:
        for key, value in d.items():
            result[key] = value  # type: ignore

    return result


def get_attr_recursive(obj: Any, attr: str, *args: Any) -> Any:
    """
    from
    https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
    """
    return functools.reduce(lambda obj_, attr_: getattr(obj_, attr_, *args), [obj] + attr.split('.'))


def set_attr_recursive(obj: Any, attr: str, value: Any) -> None:
    """
    from
    https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
    """
    pre, _, post = attr.rpartition('.')
    return setattr(get_attr_recursive(obj, pre) if pre else obj, post, value)
