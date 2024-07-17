import numpy as np
from itertools import combinations

from preflibtools.properties.subdomains.pq_trees import reorder_sets


def instance_to_ci_matrix(instance):
    """
    Builds a matrix so that the instance is candidate interval if and only if the matrix has the
    consecutive ones property.

    :param instance: the instance, only the first class is used
    :type instance: preflibtools.instances.preflibinstance.CategoricalInstance
    """
    alternatives = list(instance.alternatives_name)
    matrix = np.zeros((len(instance.preferences), instance.num_alternatives), dtype=int)
    for idx, vote in enumerate(instance.preferences):
        for alt in vote[0]:
            matrix[idx][alternatives.index(alt)] = 1
    return matrix

def instance_to_matrix(instance, interval):
    # Get alternatives sorter, for columns
    alternatives = sorted(set().union(*instance))
    alternative_count = len(alternatives)
    voter_count = len(instance)
        
    if interval == 'ci' or interval == 'cei' or interval == 'vi' or interval == 'vei':
        # Create empty matrix with sizes of voters and alternatives
        M = np.zeros((voter_count, alternative_count), dtype=int)

        # Fill in matrix  
        for idx, vote in enumerate(instance):
            for alt in vote:
                M[idx][alternatives.index(alt)] = 1

        if interval == 'ci':
            return np.array(M), alternatives
        
        elif interval == 'cei':
            # Create new M to add the complements in
            new_M = []

            # Add every row and the complement of the row
            for row in M:
                comp = 1 - row
                new_M.append(row)
                new_M.append(comp)

            return np.array(new_M), alternatives
        
        elif interval == 'vi':
            # Transpose matrix
            M = np.transpose(M)

                # Voters to give result in reordererd voters
            voters = [f"V{i+1}" for i in range(voter_count)]

            return np.array(M), voters
        
        elif interval == 'vei':
            # Transpose matrix
            M = np.transpose(M)

            # Create new M to add the complements in
            new_M = []

            # Add every row and the complement of the row
            for row in M:
                comp = 1 - row
                new_M.append(row)
                new_M.append(comp)

            # Voters to give result in reordererd voters
            voters = [f"V{i+1}" for i in range(voter_count)]

            return np.array(new_M), voters
    
    elif interval == 'wsc':
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
        voters = [f"V{i+1}" for i in range(voter_count)]

        return M.transpose(), voters

def solve_consecutive_ones(matrix):
    num_rows, num_cols = matrix.shape
    # For each column, the indices where there is a 1
    columns_indices = [[] for _ in range(num_cols)]
    for row, col in np.argwhere(matrix == 1):
        columns_indices[col] = row
    try:
        result = reorder_sets(columns_indices)
    except ValueError:
            return False, None
    ordered_idx = []
    for order in result:
         for col in columns:
            if frozenset(row for row in range(num_rows) if col[row] == 1) == order:
               ordered_idx.extend(column_duplicates[col])
               unique_columns.remove(col)
               break

    return True, ordered_idx

def is_candidate_interval(instance):
    matrix, columns_labels = instance_to_matrix(instance, interval='ci')
    res, ordered_idx = solve_consecutive_ones(matrix)
    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = matrix[:, ordered_idx]

    return True, (order_result, M_result)


def is_candidate_extremal_interval(instance):
    matrix, columns_labels = instance_to_matrix(instance, interval='cei')
    res, ordered_idx = solve_consecutive_ones(matrix)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Delete all the rows with the complements (odd rows)
        idx = [i for i in range(len(matrix)) if i%2 != 0]
        matrix = np.delete(matrix, idx, axis=0)

        # Convert result back to matrix based on column index
        M_result = matrix[:, ordered_idx]

    return True, (order_result, M_result)


def is_voter_interval(instance):
    matrix, columns_labels = instance_to_matrix(instance, interval='vi')
    res, ordered_idx = solve_consecutive_ones(matrix)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = matrix[:, ordered_idx]
        

    return True, (order_result, M_result)


def is_voter_extremal_interval(instance):
    matrix, columns_labels = instance_to_matrix(instance, interval='vei')
    res, ordered_idx = solve_consecutive_ones(matrix)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Delete all the rows with the complements (odd rows)
        idx = [i for i in range(len(matrix)) if i%2 != 0]
        matrix = np.delete(matrix, idx, axis=0)

        # Convert result back to matrix based on column index
        M_result = matrix[:, ordered_idx]

    return True, (order_result, M_result)