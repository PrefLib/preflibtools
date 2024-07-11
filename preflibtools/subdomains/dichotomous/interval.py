import numpy as np
from pq_trees import reorder_sets
from itertools import combinations
from preflibtools.instances import CategoricalInstance

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

def solve_C1(M):
    # Get shape matrix
    num_rows, num_cols = M.shape

    # Get all columns to use for solving C1
    columns = [tuple(M[:, col]) for col in range(num_cols)]

    # In sagemath duplicates will be deleted, so check for duplicates to add in result
    column_duplicates = {}
    for idx, col in enumerate(columns):
        if col not in column_duplicates:
            column_duplicates[col] = []
        column_duplicates[col].append(idx)
        
    unique_columns = list(column_duplicates.keys())

    # Make frozenset of the columns indices
    columns_to_set = [frozenset(row for row in range(num_rows) if col[row] == 1) for col in unique_columns]

    # Try to solve C1
    try:
        result = reorder_sets(columns_to_set)
    except ValueError:
            return False, []

    # Check for duplicates and add the duplicates back in the result
    ordered_idx = []
    for order in result:
         for col in unique_columns:
                if frozenset(row for row in range(num_rows) if col[row] == 1) == order:
                   ordered_idx.extend(column_duplicates[col])
                   unique_columns.remove(col)
                   break
                   
    return True, ordered_idx

# Candidate Interval
def is_CI(instance_input):
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

    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='ci')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]

    return True, (order_result, M_result)

# Candidate Extremal Interval (CEI)
def is_CEI(instance_input):
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

    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='cei')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Delete all the rows with the complements (odd rows)
        idx = [i for i in range(len(M)) if i%2 != 0]
        M = np.delete(M, idx, axis=0)

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]

    return True, (order_result, M_result)


# Voter Interval (VI)
def is_VI(instance_input):
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

    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='vi')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]
        

    return True, (order_result, M_result)


# Voter Extremal Interval (VEI)
def is_VEI(instance_input):
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

    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='vei')
    
    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Delete all the rows with the complements (odd rows)
        idx = [i for i in range(len(M)) if i%2 != 0]
        M = np.delete(M, idx, axis=0)

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]

    return True, (order_result, M_result)