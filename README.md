# Preflibtools

[![PyPI Status](https://img.shields.io/pypi/v/preflibtools.svg)](https://pypi.python.org/pypi/preflibtools)
[![Build badge](https://github.com/PrefLib/preflibtools/workflows/build/badge.svg?branch=main)](https://github.com/PrefLib/preflibtools/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/PrefLib/preflibtools/branch/main/graphs/badge.svg)](https://codecov.io/gh/PrefLib/preflibtools/tree/main)

## Overview

The PrefLib-Tools is a set of Python tools developed to work with preference data from the
[PrefLib.org website](https://www.preflib.org/).

This package provides input and output operations on PrefLib instances, together with some additional functionalities
on the instances: Testing whether a Condorcet winner exists, whether the instance is single-peaked, etc...

We developed this package in the hope of making the use of PrefLib instances easy. This has been done in the same
spirit as PrefLib: Providing tools for the community with the help of the community. If you want to contribute, feel
free to create pull requests. If you have a question, a remark, or encounter a problem, please open an issue, create a
pull request etc...

The full documentation of the package can be found there: https://preflib.github.io/preflibtools/.

If, for some reasons, you are looking for the older version of the PrefLib-Tools, it is still available in the GitHub
repository [Preflib-Tools-Old](https://github.com/PrefLib/Preflib-Tools-Old).

## Installation

The installation is as easy as:

```shell
pip3 install preflibtools
```

## Documentation

The complete documentation is available [here](https://preflib.github.io/preflibtools/).

## GitHub Workflow

### Publishing on PyPI

The pipeline between GitHub and PyPI is automatised. To push a new version do the following:
- Update the `pyproject.toml` with the new version number.
- Update the `pabutools/__init__.py` with the new version number.
- On GitHub, create a new release tagged with the new version number (only admins can do that), on [this page](https://github.com/PrefLib/preflibtools/releases/new).
- You're done, the new version of the package is automatically pushed to PyPI after the creation of a GitHub release.

### Building the Docs

If the docs-source has been updated but the `docs/` folder has not, you can build the docs via
a GitHub action here: https://github.com/PrefLib/preflibtools/actions/workflows/docs.yml.
Simply click "Run workflow" and the docs will be built and the built files will be pushed back to
the server.
