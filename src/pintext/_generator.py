from collections.abc import Callable, Generator
from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass

import pint


@dataclass(slots=True)
class UnitGenerator:
    """
    A callable object which returns units objects. Stored units can be
    contextually overridden using the :meth:`~pintext.UnitGenerator.override`
    method.

    :param units:
        Stored units or generator.

    .. rubric:: Examples

    >>> ugen = UnitGenerator(ureg.m)
    >>> ugen()
    <Unit('meter')>

    Stored units can be modified, including temporarily:

    >>> with ugen.override(ureg.km):
    ...     ugen()
    <Unit('kilometer')>
    >>> ugen()
    <Unit('meter')>

    .. seealso:: :class:`~pintext.UnitContext`
    """

    #: Stored units or generator.
    units: pint.Unit | Callable[[], pint.Unit]

    def __call__(self) -> pint.Unit:
        """
        :returns:
            If ``units`` is a :class:`pint.Unit`, it is returned; if ``units``
            is a callable (typically, another :class:`~pintext.UnitGenerator`),
            the result of its evaluation will be returned.
        """
        if isinstance(self.units, pint.Unit):
            return self.units
        return self.units()

    @contextmanager
    def override(
        self, units: pint.Unit | Callable[[], pint.Unit] | str
    ) -> Generator[None]:
        """
        Temporarily override the value of ``units``. The initial value of
        ``units`` is restored upon leaving context.

        :param units:
            Temporary replacement for ``units``. String values are interpreted
            based on the unit registry of currently stored units.

        .. note::
            This context manager mutates the generator in-place and is therefore
            not thread-safe.
        """
        units_old = copy(self.units)

        if isinstance(units, str):  # Safeguard to convert strings
            current = self.units if isinstance(self.units, pint.Unit) else self.units()
            # _REGISTRY is private Pint API
            self.units = current._REGISTRY.Unit(units)
        else:
            self.units = units
        try:
            yield
        finally:
            self.units = units_old
