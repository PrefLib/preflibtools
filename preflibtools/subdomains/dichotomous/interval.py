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
    

    input_matrix = [tuple(i for i in range(len(row)) if row[i] == 1) for row in M]
    return input_matrix

    # Need later
    if interval == 'vi':
       return M, alternatives

    elif interval == 'ci':
        M = list(zip(*M))
        pass
    elif interval == 'vei':
        pass
    elif interval == 'cei':
        pass

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


    for ordering in p.orderings():
        print(ordering)


    # Print the cardinality after setting contiguity
    # print("Cardinality after:", p.cardinality())
    
    return p.orderings()



# Voter Interval (VI)
def is_VI(instance):
    # Comvert instance to matrix
    # M, alternatives = instance_to_matrix(instance, interval = 'vi')
    alternatives = sorted(set().union(*instance))

    # If input p is just the alternatives and not binary matrix (to list) it does work?
    # but why
    instances_list = [list(vote) for vote in instance]

    # Make P tree and set contiguous for all alternatives to solve consecutive ones problem
    p = P(instances_list)
    for alt in alternatives:
        # If could not solve consecutive ones than False                    # Here i already tried to use column index in set continuous or by alternative name
        if not p.set_contiguous(alt):
            return False
        p.set_contiguous(alt)
    
    

    # Get order
    order = p.ordering()

    print("CI order:", order)
    return True

# Voter Extremal Interval (VEI)
def is_VEI(instance):
    '''
    Started here but continued for VI in the meantime
    '''
    # Convert instance to matrix
    M, alternatives = instance_to_matrix(instance, interval = 'vei')
    # alternatives = sorted(set().union(*instance))
    # M = M.transpose
    # Make P tree and set contiguous for all alternatives to solve consecutive ones problem
    p = P(M)
    print(p)
    for idx, alt in enumerate(alternatives):  
        p.set_contiguous(idx)
        p.set_contiguous(alt)
    
    print(p)


    ordering = p.ordering()

    return p


# Candidate Extremal Interval (CEI)
def is_CEI(instance):
    M = instance_to_matrix(instance, interval = 'cei')
    pass




instance = [
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




def is_vei_test(matrix, alt_count):
    positions = []
    for row in matrix:
        for i in range(alt_count):
            if row[i] == 1:
                positions.append(i)
        for idx in range(len(positions) -1):
            if positions[idx]+1 != positions[idx+1]:
                return False
        positions = []

    for i in range(alt_count):
        positions = [j for j in range(len(matrix)) if matrix[j][i] == 1]
        if len(positions) > 1:
            # Check if the 1s form a contiguous block in the column         #?
            pass
    return True

res = is_vei_test(matrix, alt_count)
print(res)

instance = [
    {'C', 'D'},
    {'A', 'B', 'C'},
    {'B', 'C'},
    {'C'},
    {'D'},
    {'D'}
]
instance_to_matrix(instance, interval='vei')