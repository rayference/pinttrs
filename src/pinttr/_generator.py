from contextlib import contextmanager
from copy import copy
from typing import Callable, Union

import attrs
import pint


@attrs.define
class UnitGenerator:
    """
    A callable object which returns units objects.
    Stored units can be contextually overridden using the
    :meth:`~pinttrs.UnitGenerator.override` method.

    .. seealso:: :class:`~pinttrs.UnitContext`

    :Attributes / constructor arguments:

        **units** (:class:`pint.Unit` or :class:`Callable`) –
        Stored units or generator.
    """

    units: Union[pint.Unit, Callable] = attrs.field()

    def __call__(self) -> pint.Unit:
        """
        :returns:
            If ``units`` is a :class:`pint.Unit`, it is returned; if ``units``
            is a callable (typically, another :class:`~pinttrs.UnitGenerator`),
            the result of its evaluation will be returned.
        """
        if callable(self.units):
            return self.units()
        return self.units

    @contextmanager
    def override(self, units: Union[pint.Unit, Callable, str]) -> None:
        """
        Temporarily override the value of ``units``. The initial value of
        ``units`` is restored upon leaving context.

        :param units:
            Temporary replacement for ``units``. String values are interpreted
            based on the unit registry of currently stored units.
        """
        units_old = copy(self.units)

        if isinstance(units, str):  # Safeguard to convert strings
            if callable(self.units):
                self.units = self.units()._REGISTRY.Unit(units)
            else:
                self.units = self.units._REGISTRY.Unit(units)
        else:
            self.units = units
        try:
            yield
        finally:
            self.units = units_old
