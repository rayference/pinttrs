:hide-toc:
:layout: landing

Pintext
=======

**Date**: |today| | **Version**: |version|

*Extend* `Pint <https://pint.readthedocs.io/>`__ *with unit contexts.*

Pintext lets an application decide, at runtime, how unitless values are
interpreted.
Optional class-framework integrations for *attrs* and *pydantic* building on
that core are provided.

.. grid:: 1 1 2 3
    :gutter: 2
    :padding: 0

    .. grid-item-card:: :iconify:`material-symbols:book-2 height=1.5em` User guide
        :link: user_guide/index
        :link-type: doc

        Read the user guide.

    .. grid-item-card:: :iconify:`material-symbols:description height=1.5em` API reference
        :link: api/pintext
        :link-type: doc

        Browse the API reference.

    .. grid-item-card:: :iconify:`material-symbols:swap-horiz height=1.5em` Porting guide
        :link: porting
        :link-type: doc

        Migrate from Pinttrs.

    .. grid-item-card:: :iconify:`material-symbols:code height=1.5em` Developer guide
        :link: dev/index
        :link-type: doc

        Contribute to and maintain Pintext.

    .. grid-item-card:: :iconify:`mdi:clock height=1.5em` Changelog
        :link: changelog
        :link-type: doc

        Release history and migration notes.

    .. grid-item-card:: :iconify:`simple-icons:github height=1.5em` GitHub
        :link: https://github.com/rayference/pintext/

        Browse the source code.

Pintext is distributed under the terms of the
`MIT license <https://choosealicense.com/licenses/mit/>`_. It is written and
maintained by `Vincent Leroy <https://github.com/leroyvn>`_, with development
supported by `Rayference <https://www.rayference.eu>`_, and is a component of
the `Eradiate radiative transfer model <https://www.eradiate.eu>`_.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Use

   user_guide/index
   porting

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Reference

   api/pintext
   api/pintext.attrs
   api/pintext.pydantic

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Develop

   dev/index.md
   GitHub repository <https://github.com/rayference/pintext>

.. toctree::
   :hidden:
   :caption: About

   changelog.md
