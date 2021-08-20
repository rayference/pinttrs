"""
APIs in the style of attrs's next-generation APIs.
"""
from typing import Union

import pint
from attr import NOTHING

from ._generator import UnitGenerator
from ._make import attrib


def field(
    *,
    default=NOTHING,
    validator=NOTHING,
    repr=NOTHING,
    hash=None,
    init=True,
    metadata=None,
    converter=NOTHING,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=NOTHING,
    units: Union[None, pint.Unit, UnitGenerator] = None,
):
    """
    Identical to :func:`pinttr.ib`, except keyword-only and with some arguments
    removed.

    .. versionadded:: 21.3.0
    """
    return attrib(
        default=default,
        validator=validator,
        repr=repr,
        hash=hash,
        init=init,
        metadata=metadata,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
        units=units,
    )
