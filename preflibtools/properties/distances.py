""" This module provides functions to compute distances between orders.
"""

import numpy as np


def distance_matrix(instance, distance_function):
    """Returns a matrix of the pairwise distance between all orders of the instance.

    :param instance: The instance to take the orders from.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param distance_function: The distance function to use. It should take two orders as input.
    :type distance_function: function

    :return: A Numpy array of the pairwise distances, coordinates being the index of the orders in the order
        list of the instance.
    :rtype: numpy array
    """
    profile = instance.full_profile()
    num_voters = len(profile)
    res = np.zeros((num_voters, num_voters))
    for i in range(num_voters):
        for j in range(i + 1, num_voters):
            res[(i, j)] = distance_function(profile[i], profile[j])
            res[(j, i)] = distance_function(profile[j], profile[i])
    return res


def kendall_tau_distance(order1, order2):
    """Returns the Kendall's tau distance between two orders.

    :param order1: The first order.
    :type order1: tuple
    :param order2: The second order.
    :type order2: tuple

    :return: The Kendall's tau distance between the two orders.
    :rtype: int
    """
    if len(order1) != len(order2):
        raise ValueError(
            "Rankings must have the same length to compute their Kendall's tau distance"
        )
    res = 0
    norm = 0
    for j1 in range(len(order1)):
        for j2 in range(j1 + 1, len(order1)):
            res += order2.index(order1[j1]) > order2.index(order1[j2])
            norm += 1
    return res / norm


def spearman_footrule_distance(order1, order2):
    """Returns the Spearman's footrule distance between two orders.

    :param order1: The first order.
    :type order1: tuple
    :param order2: The second order.
    :type order2: tuple

    :return: The Spearman's footrule distance between the two orders.
    :rtype: float
    """
    if len(order1) != len(order2):
        raise ValueError(
            "Rankings must have the same length to compute their Spearman's footrule distance"
        )
    res = 0
    for j in range(len(order1)):
        res += abs(j - order2.index(order1[j]))
    return res / np.floor(len(order1) ** 2 / 2)


def sertel_distance(order1, order2):
    """Returns the Sertel's distance between two orders.

    :param order1: The first order.
    :type order1: tuple
    :param order2: The second order.
    :type order2: tuple

    :return: The Sertel's distance between the two orders.
    :rtype: float
    """
    if len(order1) != len(order2):
        raise ValueError(
            "Rankings must have the same length to compute their Sertel's distance"
        )
    j = 0
    for j in range(len(order1)):
        if order1[j] != order2[j]:
            break
    return (len(order1) - 1 - j) / (len(order1) - 1)
