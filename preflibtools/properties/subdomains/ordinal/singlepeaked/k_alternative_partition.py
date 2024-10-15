from __future__ import annotations

from preflibtools.properties.subdomains.ordinal.singlepeaked.k_alternative_deletion import longest_single_peaked_axis, \
    get_L_sets, place

import math


def k_alt_partition_approx(instance):
    """
    Approximates a profiles k-alternative partition single-peakedness
    by continuously creating the longest possible single-peaked axis among
    the remaining alternatives using the algorithm of Erdélyi, Lackner, Pfandler (2017).

    :param instance: the instance to test for k-alternative deletion single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A list containing the axes that the algorithm has created.
    :rtype: list(list)
    """

    alternatives = list(instance.alternatives_name.keys())

    axes = []

    while len(alternatives) > 0:
        longest_axis, alternatives = longest_single_peaked_axis(instance, alternatives)

        axes.append(longest_axis)

    return axes


def k_alternative_partition_brut_force(instance, k):
    """
    Generates the lowest amount of partitions of the alternatives in a given
    profile such that when restricted to each partition, the profile is single-peaked.
    This is done by brute-forcing all admissible partitions in a DFS fashion.

    :param instance: the instance to test for k-alternative deletion single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param k: The maximum number of partitions
    :type k: int

    :return: A list containing single-peaked axes representing the optimal partitions
    :rtype: list(list)  
    """

    alternatives = list(instance.alternatives_name.keys())
    m = len(alternatives)
    unique_votes = [vote for vote, _ in instance.flatten_strict()]

    # optimum number of partitions can't exceed floor(m / 2)
    if k > math.floor(m / 2):
        k = math.floor(m / 2)

    # Construct L sets
    L = get_L_sets(alternatives, unique_votes)

    L_segmented = {i: singleton_pair_combinations(list(alts)) for i, alts in L.items()}

    partitions = dfs(0, [], None, m, k, L_segmented, unique_votes)

    if partitions is not None:
        for axes in partitions:
            axes.remove(None)

    return partitions


def dfs(i, axes, shortest, m, k, L, unique_votes):
    """
    A helper function of the k-alternative partition algorithm.
    Traverses the search-space recursively by gathering all possible ways
    the current incomplete axes may be extended, finding all extensions that remain
    single-peaked, passing the extended axes into the next function in a depth first search
    manner and returning the result with the lowest number of partitions.

    :param i: current depth/step of the procedure
    :type i: int
    :param axes: list of incomplete axes that need to be completed
    :type axes: list(list)
    :param shortest: shortest complete partition that has been found so far
    :type shortest: None/list(list)
    :param m: last step/lowest depth of the procedure
    :type m: int
    :param k: bound on the number of partitions
    :type k: int
    :param L: dict containing all ways to add the alternatives 
    to be placed at step i unto the axes.
    :type L: dict
    :param unique_votes: The unique orders within the profile.
    :type unique_votes: list(list)

    :return: list of the lowest number of partitions that could be created from
        the given axes.
    :rtype: list(list)
    """

    # All alternatives have been placed at step m
    if i == m:
        return axes

    # Get all ways to split the alternatives to be placed at step i
    extensions = L[i + 1]

    for extension in extensions:

        # Ignore partitions that are too large
        if len(extension) > k:
            continue

        # Find all ways to extend the axes with the given partition of new alternatives
        new_axes = extend(axes, extension, unique_votes, k)

        for ax in new_axes:
            # Ignore this partition if it is already longer than the shortest complete partition
            if shortest is None or len(ax) < len(shortest):
                completed_partitions = dfs(i + 1, ax, shortest, m, k, L, unique_votes)

                # Check if it is shorter than current shortest
                if completed_partitions is not None:
                    if shortest is None or len(shortest) > len(completed_partitions):
                        shortest = completed_partitions

    return shortest


def extend(axes, extension, unique_votes, k):
    """
    A helper function of the k-alternative partition algorithm.
    Finds and returns all ways to place a set of singleton and pairs of alternatives
    unto a list of incomplete axes, such that single-peakedness is not violated.

    :param axes: list of incomplete axes that need to be extended
    :type axes: list(list)
    :param extension: list of singletons and pairs of alternatives that need to be placed
    :type extension: list
    :param unique_votes: The unique orders within the profile.
    :type unique_votes: list(list)
    :param k: The maximum number of partitions
    :type k: int

    :return: List of lists of new incomplete axes obtained after placing extensions
    :rtype: list(list(list))
    """
    queue = [[axes, []]]

    # For each singleton/pair, find all the locations it can be placed in
    for alt in extension:

        new_queue = []

        if len(queue) > 0:
            for unused_axes, used_axes in queue:

                # Check if it can be placed in an axis that has not been extended yet
                for axis in unused_axes:
                    new_axis, _ = place(axis, alt, unique_votes)

                    # If yes, add this instance to the queue for the next alternative, this axis is no longer useable in this instance
                    if new_axis != axis:
                        new_unused_axes = [a for a in unused_axes if a != axis]
                        new_used_axes = used_axes + [new_axis]

                        new_queue.append([new_unused_axes, new_used_axes])

                # Also check if there is room to create a new incomplete axis with this extension
                if len(unused_axes) + len(used_axes) < k:
                    new_axis, _ = place([None], alt, unique_votes)

                    if new_axis != [None]:
                        new_used_axes = used_axes + [new_axis]

                        new_queue.append([unused_axes, new_used_axes])

        queue = new_queue

    # For each succesful extension, combine the used and unused axes
    new_axes = []
    if len(queue) > 0:
        for remaining_axes, used_axes in queue:
            new_axes.append(remaining_axes + used_axes)

    return new_axes


def singleton_pair_combinations(items):
    """
    A helper function of the k-alternative partition algorithm.
    Constructs all partitions into singletons and unordered pairs of a given
    set of items.
    """

    if len(items) == 0:
        return [[]]
    elif len(items) == 1:
        return [[tuple(items)]]
    else:
        combis = []

        # Take the first element
        head = items.pop(0)

        # Give it a pair and find all partitions into singletons and unordered pairs of the remaining items
        for pairing in items:
            pair = (head, pairing)

            remaining_items = [i for i in items if i != pairing]

            tail_combis = singleton_pair_combinations(remaining_items)

            for combi in tail_combis:
                combis.append([pair] + combi)

        # Let it be a singleton and find all partitions into singletons and unordered pairs of the remaining items
        other_combis = singleton_pair_combinations(items)

        # compile all results partitions
        for combi in other_combis:
            combis.append([(head,)] + combi)

        return combis
