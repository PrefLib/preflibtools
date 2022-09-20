============
Preflibtools
============

.. image:: https://img.shields.io/pypi/v/preflibtools.svg
        :target: https://pypi.python.org/pypi/preflibtools
        :alt: PyPI Status

.. image:: https://github.com/PrefLib/preflibtools/workflows/build/badge.svg?branch=main
        :target: https://github.com/PrefLib/preflibtools/actions?query=workflow%3Abuild
        :alt: Build Status

.. image:: https://readthedocs.org/projects/docs/badge/?version=latest
        :target: https://www.docs.preflib.org/
        :alt: Documentation Status

.. image:: https://codecov.io/gh/PrefLib/preflibtools/branch/main/graphs/badge.svg
        :target: https://codecov.io/gh/PrefLib/preflibtools/tree/main
        :alt: Code Coverage

Overview
========

The PrefLib-Tools is a set of Python tools developed to work with preference data from the
`PrefLib.org website <https://www.preflib.org/>`_.

This package provides input and output operations on PrefLib instances, together with some additional functionalities
on the instances: Testing whether a Condorcet winner exists, whether the instance is single-peaked, etc...

We developed this package in the hope of making the use of PrefLib instances easy. This has been done in the same
spirit as PrefLib: Providing tools for the community with the help of the community. If you want to contribute, feel
free to create pull requests. If you have a question, a remark, or encounter a problem, please open an issue, create a
pull request etc...

The full documentation of the package can be found there: `http://www.docs.preflib.org <http://www.docs.preflib.org/>`_.

If, for some reasons, you are looking for the older version of the PrefLib-Tools, it is still available in the GitHub
repository `Preflib-Tools-Old <https://github.com/PrefLib/Preflib-Tools-Old>`_.

Usage
=====

Ordinal Preferences
-------------------

.. include:: docs/source/ex_ordinal.rst

Categorical Preferences
-----------------------

.. include:: docs/source/ex_categorical.rst

Matching Preferences
--------------------

.. include:: docs/source/ex_matching.rst

Requirements
============

This package relies of the following ones:

* **numpy**: to deal with array and math-related functions (random generator, factorial, etc...);
* **mip**: to deal with optimisation problems (for instance closeness to single-peakedness).