import numpy as np

from preflibtools.properties.subdomains.ordinal.single_peaked.k_alternative_deletion import k_alternative_deletion, remove_alternatives
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.single_peaked.singlepeakedness import is_single_peaked
from preflibtools.instances import OrdinalInstance

from prefsampling.ordinal import singlepeaked as sp_samplers

from unittest import TestCase


def generate_k_alt_nearly_sp(num_voters, num_alternatives, k, seed=None):
    """Generates a non-single-peaked profile that becomes single-peaked after
    k alternatives are deleted. This is done by generating a single-peaked profile and
    adding extra orders such that there remain WD-structures untill k alternatives are removed.

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
        raise ValueError(
            "Cannot remove more alternatives than total."
        )

    rng = np.random.default_rng(seed)

    votes = sp_samplers.single_peaked_walsh(num_voters - (2 + k), num_alternatives, seed=seed)
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

        # test 1, sp profile
        params = {
            "num_voters" : 500,
            "num_alternatives" : 11,
            "k": 0,
            "seed" : 1
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert axis == [i for i in range(11)]
        assert candidates == []
        assert is_single_peaked(SP_instance)

        # test 2, non-sp profile, remove 4 
        params = {
            "num_voters" : 500,
            "num_alternatives" : 11,
            "k" : 4,
            "seed" : 10
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)


        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert len(axis) == 7
        assert len(candidates) == 4
        assert is_single_peaked(SP_instance)

        # test 3, non-sp profile, remove 7 
        params = {
            "num_voters" : 10000,
            "num_alternatives" : 12,
            "k" : 7,
            "seed" : 5
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert len(axis) == 5
        assert len(candidates) == 7
        assert is_single_peaked(SP_instance)