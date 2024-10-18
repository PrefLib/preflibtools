""" This module describes procedures to sample preferences for different probability distributions.
Note that this has been updated to use the samplers provided in the
`prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ package.
"""
import math

from prefsampling.ordinal import mallows, urn, impartial, impartial_anonymous
from prefsampling.core import mixture as sampling_mixture
import numpy as np

from collections import defaultdict


def prefsampling_ordinal_wrapper(sampler, sampler_params):
    votes = sampler(**sampler_params)
    vote_map = defaultdict(lambda: 0)
    for order in votes:
        order = tuple((a,) for a in order)
        vote_map[order] += 1
    return vote_map


def generate_mallows(
    num_voters, num_alternatives, mixture, dispersions, references, norm_phi=False
):
    """Generates a profile following a mixture of Mallow's models. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int
    :param mixture: A list of the weights of each element of the mixture.
    :type mixture: list of positive numbers
    :param dispersions: A list of the dispersion coefficient of each element of the mixture.
    :type dispersions: list of float
    :param references: A list of the reference orders for each element of the mixture.
    :type references: list of tuples of tuples of int
    :param norm_phi: Computes the normalised phi values based on the dispersion coefficients given if true.
        Defaults to False.
    :type norm_phi: bool

    :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
        the given order as their preferences.
    :rtype: dict
    """
    if len(mixture) != len(dispersions) or len(mixture) != len(references):
        raise ValueError("Parameters of Mallows' mixture do not have the same length.")
    # We normalize the mixture so that it sums up to 1
    mixture_sum = sum(mixture)
    if mixture_sum != 1:
        mixture = [m / mixture_sum for m in mixture]

    params = {
        "num_voters": num_voters,
        "num_candidates": num_alternatives,
        "samplers": [mallows] * len(mixture),
        "weights": mixture,
        "sampler_parameters": [
            {
                "phi": dispersions[i],
                "central_vote": np.array([a for c in references[i] for a in c]),
                "normalise_phi": norm_phi,
            }
            for i in range(len(mixture))
        ],
    }
    return prefsampling_ordinal_wrapper(
        sampling_mixture,
        params,
    )


def generate_mallows_mix(num_voters, num_alternatives, num_references, norm_phi=True):
    """Generates a profile following a mixture of Mallow's models for which reference points and dispersion
    coefficients are independently and identically distributed. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int
    :param num_references: Number of element
    :type num_references: int
    :param norm_phi: Uses the normalised phi value if true, and just a uniform distribution otherwise. Defaults to True.
    :type norm_phi: bool

    :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
        the given order as their preferences.
    :rtype: dict
    """
    mixture = []
    dispersions = []
    references = []
    for i in range(num_references):
        references.append(tuple(generate_IC(1, num_alternatives))[0])
        phi = round(np.random.rand(), 5)
        dispersions.append(phi)
        mixture.append(np.random.randint(1, 101))
    mixture = [i / sum(mixture) for i in mixture]
    return generate_mallows(
        num_voters, num_alternatives, mixture, dispersions, references, norm_phi
    )


def generate_urn(num_voters, num_alternatives, replace):
    """Generates a profile following the urn model. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int
    :param replace: The number of replacements for the urn model.
    :type replace: int

    :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
        the given order as their preferences.
    :rtype: dict
    """
    if num_alternatives > 20:
        raise ValueError(
            "Because of normalisation factors involving a factorial, we cannot run an urn sampling with "
            "more than 20 alternatives."
        )

    return prefsampling_ordinal_wrapper(
        urn,
        {
            "num_voters": num_voters,
            "num_candidates": num_alternatives,
            "alpha": replace / math.factorial(num_alternatives),
        },
    )


def generate_IC(num_voters, num_alternatives):
    """Generates a profile of strict preferences following the impartial culture. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int

    :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
        the given order as their preferences.
    :rtype: dict
    """
    return prefsampling_ordinal_wrapper(
        impartial, {"num_voters": num_voters, "num_candidates": num_alternatives}
    )


def generate_IC_anon(num_voters, num_alternatives):
    """Generates a profile of strict preferences following the anonymous impartial culture. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int

    :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
        the given order as their preferences.
    :rtype: dict
    """
    return prefsampling_ordinal_wrapper(
        impartial_anonymous,
        {"num_voters": num_voters, "num_candidates": num_alternatives},
    )


def generate_IC_ballot(num_alternatives):
    """Generates a strict order over the set of alternatives following the impartial culture. Note that all we are using the
    `prefsampling  <https://github.com/COMSOC-Community/prefsampling>`_ samplers. This is
    thus just a wrapper.

    :param num_alternatives: Number of alternatives for the sampled orders.
    :type num_alternatives: int

    :return: A strict order over the alternatives, i.e., a tuple of tuples of size 1.
    :rtype: tuple
    """

    votes = prefsampling_ordinal_wrapper(
        impartial, {"num_voters": 1, "num_candidates": num_alternatives}
    )
    return next(votes.__iter__())
