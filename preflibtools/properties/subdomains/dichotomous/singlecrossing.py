from itertools import combinations

import numpy as np

from preflibtools.properties.subdomains.consecutive_ones import solve_consecutive_ones
from preflibtools.instances import CategoricalInstance


def is_weakly_single_crossing(instance):
    """
    Tests whether the given categorical instance is weakly single crossing. Transforms a categorical instance into a
    matrix as defined in the proof of Theorem 13 in https://martin.lackner.xyz/publications/incompletesc-full.pdf and
    checks whether the matrix has the consecutive ones property.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is weakly single crossing
        and an ordering of the ballots (or None if the instance is not weakly single crossing).
    :rtype: tuple[bool, list[set] | None]
    """

    alternatives = list(instance.alternatives_name)
    all_pairs_alt = tuple(combinations(alternatives, 2))
    matrix = np.zeros((2 * len(all_pairs_alt), len(instance.preferences)), dtype=int)

    for ballot_idx, ballot in enumerate(instance.preferences):
        pair_idx = 0
        approved_alts = ballot[0]
        for a, b in all_pairs_alt:
            if a in approved_alts and b not in approved_alts:
                matrix[pair_idx, ballot_idx] = 1
            elif b in approved_alts and a not in approved_alts:
                matrix[pair_idx + 1, ballot_idx] = 1
            pair_idx += 2

    res, ordered_idx = solve_consecutive_ones(matrix)

    if res:
        return True, ordered_idx
    return False, None
