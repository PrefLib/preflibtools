.. preflibtools documentation master file, created by
   sphinx-quickstart on Wed May 18 18:58:52 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   reference/index
   about

.. include:: ../../README.rst

Modules
=======

The package provides different modules. The first set of them deal with PrefLib instances.

* **preflibtools.instances.preflibinstance**: provides the main class used to represent PrefLib instances together with a very basic graph class.
* **preflibtools.instances.sampling**: provides all kinds of methods to sample preferences using different kinds of Mallows' models and urn model's.

See the documentation of the corresponding :ref:`instances-label`.

A second set of modules introduces functions to test properties of PrefLib instances.

* **preflibtools.properties.basic**: provides a lot of small functions testing very basic properties (number of agents, size of the largest ballot...) that are mainly used for sanity checks.
* **preflibtools.properties.singlepeakedness**: provides a set of function to test whether instances represent single-peaked preferences, and related properties (closeness to single-peakedness etc...).
* **preflibtools.properties.distances**: provides a set of distances that can be computed between instances.

See the documentation of the corresponding :ref:`properties-label`.

Index
=====

The :ref:`general index <genindex>` can be found here.