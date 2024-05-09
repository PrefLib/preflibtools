import numpy as np

def instance_to_matrix(instance, interval):
    alternatives = sorted(set().union(*instance))
    alternative_count = len(alternatives)
    voter_count = len(instance)

    if interval == 'vei':
        M = np.zeros((voter_count, alternative_count))
        
        for idx, vote in enumerate(instance):
            for alt in vote:
                M[idx][alternatives.index(alt)] = 1
    
        return M

    elif interval == 'cei':
        pass
    else:
        raise KeyError("Interval must be either 'vei' or 'cei' " )


# Voter Extremal Interval (VEI)
def is_VEI(instance):
    M = instance_to_matrix(instance, interval = 'vei')
    pass


# Candidate Extremal Interval (CEI)
def is_CEI(instance):
    M = instance_to_matrix(instance, interval = 'cei')
    pass

instance = [
    {'A', 'B'},  # Voter 1 chooses alternatives A and B
    {'C'},       # Voter 2 chooses alternative C
    {'D', 'E'},  # Voter 3 chooses alternatives D and E
    {'A', 'C'}   # Voter 4 chooses alternatives A and C
]

res = instance_to_matrix(instance, 'vei')
print(res)
