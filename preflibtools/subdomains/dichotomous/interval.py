import numpy as np
from pq_trees import P
# from tests_sagemath import isC1P

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

    # print(M)
    # M = np.transpose(M)
    # print("T:", M)
    # input_M = [tuple(i for i in range(len(row)) if row[i] == 1) for row in M]

    # return input_M

    if interval == 'ci':
        input_M = [tuple(i for i in range(len(row)) if row[i] == 1) for row in M]

        # Used for testing
        # M = np.transpose(M)
        return input_M
    elif interval == 'cei':
        comp = 1 - M
        new_M = np.vstack((M, comp))
        input_M = [tuple(i for i in range(len(row)) if row[i] == 1) for row in new_M]
        return new_M
    elif interval == 'vi':
       M = np.transpose(M)
       input_M = [tuple(i for i in range(len(row)) if row[i] == 1) for row in M]
       return input_M
    elif interval == 'vei':
        M = np.transpose(M)
        comp = 1 - M
        new_M = np.vstack((M, comp))
        input_M = [tuple(i for i in range(len(row)) if row[i] == 1) for row in new_M]
        return new_M

def solve_C1(M):
    # Create P
    p = P(M)

    # print("Cardinality:", p.cardinality())

    # Make consecutive ones
    for col in range(len(matrix[0])):
        # p.set_contiguous(col)
        try:
            p.set_contiguous(col)
        except ValueError:
            return False


    # for ordering in p.orderings():
    #     print(ordering)


    # Print the cardinality after setting contiguity
    # print("Cardinality after:", p.cardinality())
    
    return p.orderings()

# Flatten the nested tuples
def flatten(ordering):
    # Check if tuple and if not more nested
    if isinstance(ordering, tuple) and not isinstance(ordering[0], tuple):
        res = [ordering]
        return tuple(res)
    
    res = []

    # Recursively flatten nested tuples
    for sub in ordering:
        res += flatten(sub)

    # Return result and make tuple again
    return tuple(res)

# Convert ordering to matrix
def C1_to_matrix(ordering, M):
    # (Maybe all orderings instead of 1 at a time)
    # for ord in ordering:
        # ord = flatten(ord)
    # print(ordering)
    # Flatten ordering
    ordering = flatten(ordering)

    # Get info to initiate matrix
    alternatives = sorted(set().union(*instance))
    alternative_count = len(alternatives)
    # This can be less then first matrix because ordering is only unique votings
    voter_count = len(ordering)
    
    # NOT CORRECT YET
    # Create empty matrix with sizes of voters and alternatives
    M = np.zeros((voter_count, alternative_count), dtype=int)

    # Possible solution
    # M = np.zeros_like(M)

    # Fill in matrix based on ordering
    for voter_idx, vote in enumerate(ordering):
        for alt_idx in vote:
            M[voter_idx, alt_idx] = 1

    return M

# Candidate Interval
def is_CI(instance):
    M = instance_to_matrix(instance, interval='ci')
    print("Check heck", M)
    res = solve_C1(M)

    if res is False:
        return False, []
    else:
        # res = next(res)
        for r in res:
            print(r)
            M = C1_to_matrix(r, instance)
            print(M)

    print(True)
    print(M)
    return True, M

# Candidate Extremal Interval (CEI)
def is_CEI(instance):
    M = instance_to_matrix(instance, interval = 'cei')
    print(M)
    res = solve_C1(M)

    if res is False:
        return False, []
    else:
        res = next(res)

    M = C1_to_matrix(res, instance)
    return True, M

# Voter Interval (VI)
def is_VI(instance):
    M = instance_to_matrix(instance, interval = 'vi')
    res = solve_C1(M)

    if res is False:
        return False, []
    else:
        res = next(res)

    M = C1_to_matrix(res, instance)
    return True, M

# Voter Extremal Interval (VEI)
def is_VEI(instance):
    M = instance_to_matrix(instance, interval = 'vei')
    res = solve_C1(M)

    if res is False:
        return False, []
    else:
        res = next(res)

    M = C1_to_matrix(res, instance)
    return True, M

instance2 = [
    {'C', 'D'},
    {'A', 'B', 'C'},
    {'B', 'C'},
    {'C'},
    {'D'},
    {'D'}
]

matrix_vei= [
    [0, 0, 1, 1],   # C D 
    [1, 1, 1, 0],   # ABC
    [0, 0, 0, 1],   # D
    [0, 0, 1, 0],   # C
    [0, 0, 0, 1],   # D
    [0, 1, 1, 0]    # B C
]

matrix_vi = [
    [0, 1, 1, 0],   # BC
    [0, 0, 1, 1],    # CD
    [0, 1, 0, 0],    # B
    [0, 0, 0, 1],    # D
    [1, 0, 0, 0],    # A
    [0, 0, 0, 1]    # D
]

matrix2 = [
    [1, 1, 1, 1, 0, 0], # ABCD
    [1, 1, 0, 0, 0, 0], # AB
    [1, 0, 0, 0, 0, 0], # A
    [0, 0, 0, 1, 1, 1]  # DEF
]
matrix_cei = list(zip(*matrix2))


matrix = [
    [1, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

matrix2 = [
    [1, 1, 1, 0],
    [0, 1, 1, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

instance = [
    {'A'},
    {'B', 'C'},
    {'A', 'D', 'E', 'F'},
    {'B', 'C', 'D'},
]
# M = instance_to_matrix(instance, interval='vei')

# solved = solve_C1(M)
# # print(M)

# for a in solved:
#     C1_to_matrix(a, instance)

is_CI(instance)

# instance_to_matrix(instance, interval='vei')