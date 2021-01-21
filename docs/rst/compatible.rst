What are "compatible units"?
============================

Pinttrs's concept of "compatible units" extends beyond the sole dimensionality.
In many contexts, adding presumably dimensionless quantities together can be
irrelevant.

The need for going beyond dimensionality actually emerged when manipulating
angles. Pint usually behaves well when converting angles:

.. doctest::

   >>> import pint
   >>> ureg = pint.UnitRegistry()
   >>> from math import pi
   >>> pi * ureg.rad + 180 * ureg.deg
   <Quantity(6.28318531, 'radian')>

However, operations involving unitless values can lead to unintuitive behaviour.
While this is quite natural:

.. doctest::

   >>> 1 + 1 * ureg.rad
   <Quantity(2, 'dimensionless')>

this can be a bit harder to anticipate:

.. doctest::

   >>> 1 + 1 * ureg.deg
   <Quantity(1.01745329, 'dimensionless')>

Things can get even more confusing when mixing angles and solid angles:

.. doctest::

   >>> 1 * ureg.deg + 1 * ureg.sr
   <Quantity(58.2957795, 'degree')>

Whaaat??? While this behaviour is, in the end, comprehensive, it emphasises the
fact that Pint doesn't recognise angle units as a special case and does not
offer facilities to prevent conversion from, say, degree to steradian. It will
neither declare as incompatible quantities which should not be mixed such as
radiance (W/m²/sr) and irradiance (W/m²).

For this reason, Pinttrs implements a stricter unit compatibility checker
function :func:`~pinttr.util.units_compatible` which will declare as
incompatible dimensionless quantities with inconvertible units. For instance,
while this will return ``True``

.. doctest::

   >>> u1 = ureg.Unit("W/m^2/sr")
   >>> u2 = ureg.Unit("W/m^2")
   >>> u1.is_compatible_with(u2)
   True

the following will not

.. doctest::

   >>> import pinttr
   >>> pinttr.util.units_compatible(u1, u2)
   False

While this does not prevent from adding radiances and irradiances, it, at least,
provides a means for checking that attributes which should be passed a radiance
will not receive an irradiance.
