import numpy as np
from pq_trees import P

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

    # Make amtrix to list for correct input for P tree
    M = M.tolist()
    print("M:", M)

    if interval == 'vi':
       return M, alternatives

    elif interval == 'ci':
        pass
    elif interval == 'vei':
        pass
    elif interval == 'cei':
        pass

# Voter Interval (VI)
def is_VI(instance):
    # Comvert instance to matrix
    M, alternatives = instance_to_matrix(instance, interval = 'vi')

    # If input p is just the alternatives and not binary matrix (to list) it does work?
    # but why
    instances_list = [list(vote) for vote in instance]

    # Make P tree and set contiguous for all alternatives to solve consecutive ones problem
    p = P(M)
    for alt in alternatives:
        # If could not solve consecutive ones than False
        if not p.set_contiguous(alt):
            return False
    
    # Get order
    order = p.ordering()
    print("VI order:", order)
    return True

# Voter Extremal Interval (VEI)
def is_VEI(instance):
    '''
    Started here but continued for VI in the meantime
    '''
    # Convert instance to matrix
    M, alternatives = instance_to_matrix(instance, interval = 'vei')
    # alternatives = sorted(set().union(*instance))

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

result = is_VI(instance)
print("VI:", result)