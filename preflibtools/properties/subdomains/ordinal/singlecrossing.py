""" This module provides procedures to check if an instance describes preferences that are single-crossing.
"""
from __future__ import annotations

from collections import defaultdict

from preflibtools.instances import OrdinalInstance
from preflibtools.properties import kendall_tau_distance


def _is_ordered_profile_single_crossing(profile: list):
    """Check if the given instance is single-crossing on the given order. Based
    on Algorithm 2 from "Preference Restrictions in Computational Social Choice:
    A Survey" (p. 54).

    :param profile: The list of orders
    :type profile: list

    :return:
        bool: whether or not the instance is single-crossing in the given order.
    """

    for i in range(1, len(profile) - 1):
        K_1_i = kendall_tau_distance(profile[0], profile[i])
        K_i_i1 = kendall_tau_distance(profile[i], profile[i + 1])
        K_1_i1 = kendall_tau_distance(profile[0], profile[i + 1])

        if (K_1_i + K_i_i1) != K_1_i1:
            return False

    return True


def is_single_crossing(instance: OrdinalInstance):
    """Check if the given instance is single-crossing based on the "Fast Recognition by Sorting"
    algorithm 4 presented in the paper "Preference Restrictions in Computational Social
    Choice: A Survey" (p. 55).

    :param instance: The instance to take the orders from.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A Boolean indicating whether the instance is single-crossing, together with the ordered
        preferences that demonstrates that the profile is single-crossing or None if the instance is not
        single-crossing.
    :rtype: Tuple(bool, list)
    """

    orders = [o for o, m in instance.flatten_strict()]

    if len(orders) <= 1:
        return True, orders

    # v_1 and v_2 will always have different preferences due to multiplicity
    # being recorded in the instance
    v_1 = orders[0]
    v_2 = orders[1]

    # Kendall-Tau distance between the first two voters
    k_dist = kendall_tau_distance(v_1, v_2)

    # array indexed by voters
    scores = defaultdict(lambda: 0)
    scores[v_2] = k_dist

    for order in orders[2:]:
        k_dist_1 = kendall_tau_distance(v_1, order)
        k_dist_2 = kendall_tau_distance(v_2, order)

        if k_dist_1 + k_dist_2 == k_dist:
            # i goes in between 1 and 2
            scores[order] = k_dist_1
        elif k_dist + k_dist_2 == k_dist_1:
            # i goes after 2
            scores[order] = k_dist_1
        elif k_dist_1 + k_dist == k_dist_2:
            # i goes before 1
            scores[order] = -k_dist_1
        else:
            # instance is not single-crossing
            return False, None

    # order voters by score
    n = len(instance.orders)
    m = len(instance.alternatives_name)

    voters_order = []
    if n < m:
        voters_order = sorted(orders, key=lambda x: scores[x])
    elif n >= m:
        array = [[] for _ in range(-m**2, m**2 + 1)]
        for order in orders:
            array[int(scores[order] + m**2)].append(order)
        # line 6: XOR on all the elements of B_arr
        voters_order = [elem[0] for elem in array if elem != []]

    # check if the computed order is single-crossing
    if _is_ordered_profile_single_crossing(voters_order):
        return True, voters_order
    else:
        return False, None


def is_single_crossing_conflict_sets(instance):
    """Tests whether the instance describe a profile of single-crossed preferences.

    :param instance: The instance to take the orders from.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A boolean indicating whether the instance is single-crossed or no.
    :rtype: bool
    """

    def prefers(a, b, o):
        return o.index(a) < o.index(b)

    def conflict_set(o1, o2):
        res = set([])
        for i in range(len(o1)):
            for j in range(i + 1, len(o1)):
                if (prefers(o1[i], o1[j], o1) and prefers(o1[j], o1[i], o2)) or (
                    prefers(o1[j], o1[i], o1) and prefers(o1[i], o1[j], o2)
                ):
                    res.add((min(o1[i][0], o1[j][0]), max(o1[i][0], o1[j][0])))
        return res

    def is_SC_with_first(i, profile):
        for j in range(len(profile)):
            for k in range(len(profile)):
                conflict_ij = conflict_set(profile[i], profile[j])
                conflict_ik = conflict_set(profile[i], profile[k])
                if not (
                    conflict_ij.issubset(conflict_ik)
                    or conflict_ik.issubset(conflict_ij)
                ):
                    return False
        return True

    for i in range(len(instance.orders)):
        if is_SC_with_first(i, instance.orders):
            return True
    return False
