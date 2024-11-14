import random

import numpy as np

from preflibtools.properties.subdomains.ordinal.singlepeaked.k_alternative_deletion import (
    k_alternative_deletion,
    remove_alternatives,
)
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.singlepeaked.singlepeakedness import (
    is_single_peaked,
)
from preflibtools.instances import OrdinalInstance

from prefsampling.ordinal import singlepeaked as sp_samplers

from unittest import TestCase


def generate_k_alt_nearly_sp(num_voters, num_alternatives, k, seed=None):
    """Generates a non-single-peaked profile that becomes single-peaked after
    k alternatives are deleted. This is done by generating a single-peaked profile and
    adding extra orders such that there remain WD-structures until k alternatives are removed.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives
    :type num_alternatives: int
    :param k: Number of alternatives that violate single-peakedness.
    :type k: int
    :param seed: Seed for numpy random number generator
    :type seed: int

    :return:
    :rtype: list(list)
    """
    if num_voters < (2 + k):
        raise ValueError(
            f"Must need at least {2 + k} votes for {k}-alternative deletion"
        )

    if k > num_alternatives:
        raise ValueError("Cannot remove more alternatives than total.")

    rng = np.random.default_rng(seed)

    votes = sp_samplers.single_peaked_walsh(
        num_voters - (2 + k), num_alternatives, seed=seed
    )
    axis = [i for i in range(num_alternatives)]

    votes.append(axis)
    votes.append(list(reversed(axis)))

    alternatives_to_remove = rng.choice(axis[1:-1], k, replace=False)

    for alt in alternatives_to_remove:
        new_vote = [a for a in axis if a != alt]
        new_vote.append(alt)
        votes.append(new_vote)

    return votes


class TestKAlternativeDeletion(TestCase):
    def test_alt_deletion_single_peaked(self):
        for _ in range(30):
            num_voters = random.randint(100, 500)
            num_alternatives = random.randint(5, 12)
            k = random.randint(0, num_alternatives - 2)
            with self.subTest(
                num_voters=num_voters, num_alternatives=num_alternatives, k=k
            ):
                params = {
                    "num_voters": num_voters,
                    "num_alternatives": num_alternatives,
                    "k": k,
                    "seed": 1,
                }
                vote_map = prefsampling_ordinal_wrapper(
                    generate_k_alt_nearly_sp, params
                )
                instance = OrdinalInstance()
                instance.append_vote_map(vote_map)

                axis, candidates = k_alternative_deletion(instance)
                sp_instance = remove_alternatives(instance, candidates)

                self.assertEqual(len(axis), num_alternatives - k)
                self.assertEqual(len(candidates), k)
                self.assertTrue(is_single_peaked(sp_instance))
