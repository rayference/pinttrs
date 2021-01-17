from pint import DimensionalityError


class UnitsError(DimensionalityError):
    """Raised when encountering issues with units (can be raised even when
    DimensionalityError would not).
    """
