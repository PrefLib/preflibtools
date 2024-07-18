from itertools import combinations

import numpy as np

from interval import solve_consecutive_ones
from preflibtools.instances import CategoricalInstance


def instance_to_matrix(instance, interval):
    # Get alternatives sorter, for columns
    alternatives = sorted(set().union(*instance))
    alternative_count = len(alternatives)
    voter_count = len(instance)

    if interval == 'wsc':
        # Find all possible combinations of alternative pairs
        all_comb = list(combinations(alternatives, 2))
        comb_count = len(all_comb)

        # Init the matrix, for all votes by 2 times the alternative pairs
        M = np.zeros((voter_count, comb_count * 2), dtype=int)

        # Loop over all votes
        for vote_idx, vote in enumerate(instance):

            # Keep track of col index to fill in for every two columns
            col_idx = 0

            # For every pair of alternatives, put correct value in matrix.
            for a, b in all_comb:
                if a in vote and b not in vote:
                    M[vote_idx, col_idx] = 1
                elif b in vote and a not in vote:
                    M[vote_idx, col_idx + 1] = 1

                # Increase col index per 2
                col_idx += 2

        # Voters to give result in reordererd voters
        voters = [f"V{i + 1}" for i in range(voter_count)]

        return M.transpose(), voters


def is_WSC(instance_input):
    if isinstance(instance_input, CategoricalInstance):
        # Convert categorical instance to usable format
        instance = []
        for p in instance_input.preferences:
            preferences = p
            pref_set = set(preferences[0])
            if len(pref_set) > 0:
                instance.append(pref_set)
    else:
        instance = instance_input

    # Get matrix and labels
    M, columns_labels = instance_to_matrix(instance, interval='wsc')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_consecutive_ones(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]
    
    return True, (order_result, M_result)