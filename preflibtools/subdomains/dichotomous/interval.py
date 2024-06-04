import numpy as np
from pq_trees import reorder_sets

def instance_to_matrix(instance, interval):
    # Get alternatives sorter, for columns
    alternatives = sorted(set().union(*instance))
    alternative_count = len(alternatives)
    voter_count = len(instance)
    
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
        M = []
        
        for vote in instance:
            row = []
            for i in range(alternative_count):
                for j in range(i + 1, alternative_count):
                    a = alternatives[i]
                    b = alternatives[j]

                    if a in vote and b not in vote:
                        row.append(1)
                        row.append(0)
                    elif b in vote and a not in vote:
                        row.append(0)
                        row.append(1)
                    else:
                        row.append(0)
                        row.append(0)
            
            M.append(row)

        M = np.array(M)
        M = M.transpose()

        # Voters to give result in reordererd voters
        voters = [f"V{i+1}" for i in range(voter_count)]
        return np.array(M), voters


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

'''
Example usage:
res, order_result, M_result = is_CI(instance, show_result=True, show_matrix=True)
order_result = result[0]
M_result = result[1]
print("Result:", res)
print("Order result:", order_result)
print("Result Matrix:\n", M_result)
'''

# Candidate Interval
def is_CI(instance, show_result=True, show_matrix=True):
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

    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])

# Candidate Extremal Interval (CEI)
def is_CEI(instance, show_result=True, show_matrix=True):
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

    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])


# Voter Interval (VI)
def is_VI(instance, show_result=True, show_matrix=True):
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
        

    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])


# Voter Extremal Interval (VEI)
def is_VEI(instance, show_result=True, show_matrix=True):
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

    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])
        
def is_WSC(instance, show_result=True, show_matrix=True):
    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='wsc')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]
    
    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])


instance_CI = [
    {'A', 'D', 'E', 'F'},
    {'C', 'D'},
    {'A', 'D'},
    {'B', 'C'}
]

instance_CEI = [
    {'A'},
    {'A', 'B', 'C', 'D'},
    {'D', 'E', 'F'},
    {'A', 'B'},
]
instance_CEI = [
    {'A'},
    {'A', 'D', 'F', 'B'},
    {'C', 'E'},
    {'B', 'C', 'E'}
]

instance_VEI = [
    {'A', 'B', 'C'},
    {'B', 'C'},
    {'C'},
    {'D', 'C'},
    {'D'}, 
    {'D'}
]

instance_VI = [
    {'A'},
    {'B'},
    {'B', 'C'},
    {'D', 'C'},
    {'D'}, 
    {'D'}
]

instance_VEI = [
    {'A', 'C'},
    {'A', 'B'},
    {'A', 'B'},
    {'C'}, 
    {'C', 'D'},
    {'C', 'D'},
]

instance_WSC = [
    {'A', 'C'},
    {'B'}
]

# res, result = is_WSC(instance_VEI)
# order_result = result[0]
# M_result = result[1]
# print("Result:", res)
# print("Order result:", order_result)
# print("Result Matrix:\n", M_result)