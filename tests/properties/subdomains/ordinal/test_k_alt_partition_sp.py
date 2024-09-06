import numpy as np

from preflibtools.properties.subdomains.ordinal.singlepeaked.k_alternative_partition import k_alternative_partition_brut_force
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.instances import OrdinalInstance

from prefsampling.ordinal import singlepeaked as sp_samplers

from unittest import TestCase


def generate_k_alt_partition_sp(num_voters, partitions, seed=None):
    """Generates a profile that is k-alternative partition single-peaked.
    This is done by merging the votes of k different single-peaked profiles
    and adding votes such that the alternatives in one profile create WD-structure
    with all pairs of alternatives in the other profiles.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param partitions:  A list containing the number of alternatives in each partition
    :type partitions: list(int)
    :param seed: Seed for numpy random number generator
    :type seed: int

    :return:
    :rtype: list(list)
    """

    rng = np.random.default_rng(seed)

    # Create axes
    axes = []
    m = 0

    for n in partitions:
        new_axis = np.array([alt for alt in range(m, m + n)])
        m += n

        axes.append(new_axis)

    # Create sp profile for each partition
    seperate_profiles = []

    for n, axis in zip(partitions, axes):
        votes = sp_samplers.single_peaked_walsh(num_voters, n, seed=seed)

        for i in range(num_voters):
            votes[i] = axis[votes[i]].tolist()

        seperate_profiles.append(votes)

    # Merge profiles
    vote_ids = []
    for i, n in enumerate(partitions):
        vote_ids += [i for _ in range(n)]

    merged_profile = []

    for i in range(num_voters):
        vote = []
        shuffled_vote_ids = vote_ids[:]
        rng.shuffle(shuffled_vote_ids)

        for id in shuffled_vote_ids:
            alt = seperate_profiles[id][i].pop(0)
            vote.append(alt)

        merged_profile.append(vote)

    # E profiles, WD-obstructing votes

    for pivot_axis in axes:
        if len(pivot_axis) < 2:
            continue

        other_axes = []
        for ax in axes:
            if not np.array_equal(pivot_axis, ax):
                other_axes.extend(ax)

        r_other_axes = list(reversed(other_axes))

        merged_profile.append(np.concatenate((pivot_axis, other_axes)))
        merged_profile.append(np.concatenate((pivot_axis, r_other_axes)))
        merged_profile.append(np.concatenate((other_axes, pivot_axis)))

    return merged_profile


def generate_counter_example():
    sp_votes = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5, 6, 10, 7, 8, 9],
        [10, 9, 8, 7, 4, 3, 2, 1, 0, 5, 6],
        [0, 1, 2, 3, 4, 10, 5, 6, 7, 8, 9],
        [0, 1, 2, 3, 4, 10, 6, 5, 7, 8, 9],
        [0, 5, 6, 1, 2, 3, 4, 10, 7, 8, 9],
        [4, 5, 6, 3, 2, 1, 0, 10, 7, 8, 9],
    ]

    return sp_votes


class TestKAlternativesPartition(TestCase):
    def test_alt_partition_single_peaked(self):

        # test 1, sp profile
        params = {
            "num_voters": 400,
            "partitions": [11],
            "seed": 2
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        partitions = k_alternative_partition_brut_force(instance, 5)

        assert len(partitions) == 1

        # test 2, non-sp profile, 5 partitions
        params = {
            "num_voters": 400,
            "partitions": [6, 3, 2, 4, 1],
            "seed": 2
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)


        partitions = k_alternative_partition_brut_force(instance, 7)

        assert len(partitions) == 5
        
        # test 3, non-sp profile, 7 partitions 
        params = {
            "num_voters": 400,
            "partitions": [7, 2, 2, 2, 5, 2, 1],
            "seed": 5
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        partitions = k_alternative_partition_brut_force(instance, 8)

        assert len(partitions) == 7
