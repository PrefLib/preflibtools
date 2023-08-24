=====
Usage
=====

We present below several examples of how to use the PrefLib-Tools. Further information about all the functions and
classes can be found in the reference.

PrefLib Instances
=================

We use different Python classes to deal with the different types of data that are hosted on
`PrefLib.org <https://www.preflib.org/>`_. All these classes inherit from :code:`PrefLibInstance`, the abstract
class that implements all the basic functionalities common to all the others. Let us first discuss the class
:code:`PrefLibInstance`, the other classes will be introduced later.

The most important functionality, is the ability to read and parse PrefLib data. We provide several ways to do so, as
illustrated below.

.. code-block:: python

    from preflibtools.instances import PrefLibInstance

    instance = PrefLibInstance()

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

Ordinal Preferences
===================

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
        multiplicity = instance.multiplicity[order]
    instance.num_unique_orders

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

    # Some statistical culture we provide, here for 5 voters and 10 alternatives
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


Categorical Preferences
=======================
Categorical preferences represent scenario in which voters were asked to place alternatives into some categories.
It is also assumed that there is an ordering of the categories inducing some preference between them.
The typical example of categorical preferences is approval ballots, in which the categories are YES and NO.

This types of preferences are represented using the :code:`CategoricalInstance` class.

.. code-block:: python

    from preflibtools.instances import CategoricalInstance

    instance = CategoricalInstance()
    instance.parse_url("https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat")

    # Additional members of the class are related to the categories themselves
    instance.num_categories
    for cat, cat_name in instance.categories_name.items():
        category = cat
        name_of_the_category = cat_name
    # But also to the preferences
    for p in instance.preferences:
        preferences = p
        multiplicity = instance.multiplicity[p]
    instance.num_unique_preferences

Matching Preferences
====================

Matching preferences cover settings in which agents are to be matched to one another, and they have affinity scores
between each others. The typical example for such preferences hosted on `PrefLib.org <https://www.preflib.org/>`_ is
that of kidney transplant where donors and patients are to be matched. The class :code:`MatchingInstance` covers these.

This class inherits both from :code:`PrefLibInstance` and from :code:`WeightedDiGraph`. This means that on top of the
usual instance machinery, it also has all the graph related members and methods.

.. code-block:: python

    from preflibtools.instances import MatchingInstance

    instance = MatchingInstance()
    instance.parse_url("https://www.preflib.org/static/data/kidney/00036-00000001.wmd")

    # The instance has a single new member: the number of edges in the graph
    instance.num_edges

    # ...and an adjacency list implementation of the weighted directed graph
    instance.nodes() # returns the set of nodes
    instance.edges() # returns the set of edges in the format (n1, n2, weight)
    instance.neighbours(n) # returns the neighbours of node n
    instance.outgoing_edges(n) # returns the edges going out of n
    instance.add_node(n) # to add a node n
    instance.add_edge(n1, n2, weight) # to add the edge (n1, n2, weight)
