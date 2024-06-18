from singlecrossing import is_WSC
from test_interval import *
from partition_tests import generate_2PART_instances
import random
from tqdm import trange
from itertools import combinations

def generate_WSC_instance(alt,voters):
    # Make a list of all alternaitves
    alternatives = [i for i in range(alt)]

    # Find all possible combinations of alternative pairs
    all_comb = list(combinations(alternatives, 2))
    # Init the voters with emtpy votes
    instance = [[] for _ in range(voters)]

    # Group size for all even group sizes
    group_size = voters // 3

    # Make the groups and the voters that belong in that group
    V1 = [v for v in range(group_size)]
    V2 = [v for v in range(group_size, len(instance) - group_size)]
    V3 = [v for v in range(len(instance) - group_size + 1, len(instance))]

    # Foralll possible combinations add something to every group V1, V2, V3
    for a, b in all_comb:

        # Group V1 add aproval vote of a
        for v in V1:
            instance[v].append(a)

        # Group V2 add aproval vote of b
        for v in V2:
            instance[v].append(b)

        # Group V3 add either both or none depending on random choice
        for v in V3:
            choice = random.randint(0,1)
            if choice == 1:
                instance[v].append(a)
                instance[v].append(b)
            # Else disapprove vote of both so add nothing


    return instance

# print("Testing positive examples WSC")
# for _ in trange(1000):
#     a = random.randint(10, 40)
#     alternatives = [i for i in range(a)]
#     v = random.randint(5, len(list(combinations(alternatives, 2))))
#     instance = generate_WSC_instance(a, v)
#     res, _ = is_WSC(instance)
#     assert res == True

# print("Testing positive examples WSC")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_2PART_instances(a, v)
#     res, _ = is_WSC(instance)
#     assert res == True

# print("Testing negative examples WSC (not CI)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CI_instances(a, v)
#     res, _ = is_WSC(instance)
#     assert res == False

# print("Testing negative examples WSC (T1)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T1(a)
#     res, _ = is_WSC(instance)
#     assert res == False

# print("Testing negative examples WSC (T2)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, _ = is_WSC(instance)
#     assert res == False

# print("Testing negative examples WSC (T3)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, _ = is_WSC(instance)
#     assert res == False

# print("Testing negative examples WSC (T4)")
# for _ in trange(1):
#     a = random.randint(5, 100)
#     instance = instance_NOT_CI_CEI_T4
#     res, _ = is_WSC(instance)
#     assert res == False

# print("Testing negative examples WSC (T5)")
# for _ in trange(1):
#     a = random.randint(5, 100)
#     instance = instance_NOT_CI_CEI_T5
#     res, _ = is_WSC(instance)
#     assert res == False

