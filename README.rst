============
Preflibtools
============

.. image:: https://img.shields.io/pypi/v/preflibtools.svg
        :target: https://pypi.python.org/pypi/preflibtools
        :alt: PyPI Status

.. image:: https://github.com/PrefLib/preflibtools/workflows/build/badge.svg?branch=main
        :target: https://github.com/PrefLib/preflibtools/actions?query=workflow%3Abuild
        :alt: Build Status

.. image:: https://github.com/PrefLib/preflibtools/workflows/docs/badge.svg?branch=main
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

PrefLib Instances
-----------------

.. inclusion-marker-instance-begin

We use different Python classes to deal with the different types of data that are hosted on
`PrefLib.org website <https://www.preflib.org/>`_. All these classes inherit from :code:`PrefLibInstance`, the abstract
class that implements all the basic functionalities common to all the others. Let us first discuss the class
:code:`PrefLibInstance`, the other classes will be introduced later.

The most important functionality, is the ability to read and parse PrefLib data. We provide several ways to do so, as
illustrated below.

.. code-block:: python

    from preflibtools.instance import PrefLibInstance

    # The instance can be populated either by reading a file, or from an URL.
    instance = PrefLibInstance()
    instance.parse_file("00001-00000001.soi")
    instance.parse_url("https://www.preflib.org/static/data/irish/00001-00000001.soi")

:code:`PrefLibInstance` also stores most of the metadata about the data file.

.. code-block:: python

    # Path to the original file, and the name of the file
    instance.file_path
    instance.file_name
    # The type of the instance and its modification type
    instance.data_type
    instance.modification_type
    # Some potentially related files
    instance.relates_to
    instance.related_files
    # The title of the data file and its description (mainly empty, on purpose)
    instance.title
    instance.description
    # Some historical landmark about the data file
    instance.publication_date
    instance.modification_date
    # The number of alternatives and their names
    instance.num_alternatives
    for alt, alt_name in instance.alternatives_name.items():
        alternative = alt
        name = alt_name
    # The number of voters
    instance.num_voters

Finally, :code:`PrefLibInstance` also provide the basic functions to write the instance.

.. code-block:: python

    instance.write(path_to_the_file)

As said before, :code:`PrefLibInstance` is an abstract class, so all the actual stuff only happens in what comes next.

.. inclusion-marker-instance-end

Ordinal Preferences
-------------------

.. inclusion-marker-ordinal-begin

Preferences that can be represented as orders over the alternatives are called ordinal. The orders can be partial,
and/or weak. All these preferences are represented using the class :code:`OrdinalInstance`. It implements the basic
functions required by :code:`PrefLibInstance` and provide additional metadata that are illustrated below.

.. code-block:: python

    from preflibtools.instances import OrdinalInstance

    # We can populate the instance by reading a file from PrefLib.
    # You can do it based on a URL or on a path to a file
    instance = OrdinalInstance()
    instance.parse_file("00001-00000001.soi")
    instance.parse_url("https://www.preflib.org/static/data/irish/00001-00000001.soi")

    # Additional members of the class are the orders,  their multiplicity and the number of unique orders
    for o in instance.orders:
        order = o
        multiplicity = instance.order_multiplicity[order]
    instance.num_unique_order

We represent orders as tuples of tuples (we need them to be hashable), i.e., it is a vector of sets of alternatives
where each set represents an indifference class for the voter. Here are some examples of orders.

.. code-block:: python

    # The strict and complete order 1 > 2 > 0
    strict_order = ((1,), (2,), (0,))
    # The weak and complete order (1, 2) > 0 > (3, 4)
    weak_order = ((1, 2), (0,), (3, 4))
    # The incomplete an weak order (1, 2) > 4
    incomplete_order = ((1, 2), (4,))

Now that we know how orders are represented, we can see some example of how to handle orders within the instance.

.. code-block:: python

    # Adding preferences to the instance, using different formats
    # Simply a list of orders
    extra_orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(extra_orders)
    # A vote map, i.e., a dictionary mapping orders to their multiplicity
    extra_vote_map = {((0,), (1,), (2,)): 3, ((2,), (0,), (1,)): 2}
    instance.append_vote_map(extra_vote_map)

    # We can access the full profile, i.e., with orders appearing several times
    # (according to their multiplicity)
    instance.full_profile()

    # If we are dealing with strict orders, we can flatten the orders so that ((0,), (1,), (2,))
    # is rewritten as (0, 1, 2). This return a list of tuple(order, multiplicity).
    instance.flatten_strict()

    # We can access the profile as a vote map
    instance.vote_map()

An instance can be populated by reading a file, but also through some sampling procedures that we provide.

.. code-block:: python

    # Some tatistical culture we provide, here for 5 voters and 10 alternatives
    instance = OrdinalInstance()
    instance.populate_mallows_mix(5, 10, 3)
    instance.populate_urn(5, 10, 76)
    instance.populate_IC(5, 10)
    instance.populate_IC_anon(5, 10)

To finish, we may want to test some properties of the instance. Let's start with some basic ones.

.. code-block:: python

    from preflibtools.properties import borda_scores, has_condorcet

    # Let's check the Borda scores of the alternatives
    borda_scores(instance)
    # We can also check if the instance has a Condorcet winner
    has_condorcet(instance)

The are plenty of methods to check for the potential single-peakedness of the instance.

.. code-block:: python

    from preflibtools.properties.singlepeakedness import *

    # We can first check if the instance is single-peaked with respect to a given
    # axis. This only works for complete orders, they can be weak though.
    is_SP = is_single_peaked_axis(instance, [0, 1, 2])
    # In general we can test for the single-peakedness of the instance:
    # In the case of strict and complete orders;
    (is_SP, axis) = is_single_peaked(instance)
    # And in the case of weak and complete order (using an ILP solver).
    (is_SP, opt_status, axis) = is_single_peaked_ILP(instance)

    # Maybe the instance is not single-peaked, but approximately. We can check how close to
    # single-peaked it is in terms of voter deletion and alternative deletion.
    (num_voter_deleted, opt_status, axis, deleted_voters) = approx_SP_voter_deletion_ILP(instance)
    (num_alt_deleted, opt_status, axis, deleted_alts) = approx_SP_alternative_deletion_ILP(instance)

We can also look into single-crossing.

.. code-block:: python

    from preflibtools.properties.singlecrossing import is_single_crossing

    # Testing if the instance is single-crossing
    is_single_crossing(instance)

Finally, we can talk about distances between the orders of the instance.

.. code-block:: python

    from preflibtools.properties.distances import distance_matrix, spearman_footrule_distance
    from preflibtools.properties.distances import kendall_tau_distance, sertel_distance

    # We can create the distance matrix between any two orders of the instance
    distance_matrix(instance, kendall_tau_distance)
    distance_matrix(instance, spearman_footrule_distance)
    distance_matrix(instance, sertel_distance)


.. inclusion-marker-ordinal-end

Categorical Preferences
-----------------------

.. inclusion-marker-categorical-begin

.. inclusion-marker-categorical-end

Matching Preferences
--------------------

.. inclusion-marker-matching-begin

.. inclusion-marker-matching-end

Requirements
============

This package relies of the following ones:

* **numpy**: to deal with array and math-related functions (random generator, factorial, etc...);
* **mip**: to deal with optimisation problems (for instance closeness to single-peakedness).