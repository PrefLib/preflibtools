from test_interval import *
import random
from tqdm import trange
from euclidean import is_DUE
from partition_tests import generate_PART_instances
from prefsampling import EuclideanSpace
from prefsampling.approval import euclidean_vcr
from test_singlecrossing import generate_WSC_instance
from test_singlecrossing import *

'''
Uncomment to run the tests
'''

# print("Testing positive examples DUE (Prefsampling)")
# for _ in trange(100):
#     a = random.randint(5, 50)
#     v = random.randint(5, 50)
#     instance = euclidean_vcr(num_voters=v, num_candidates=a, voters_radius=1/a, candidates_radius=1/a, num_dimensions=1, voters_positions=EuclideanSpace.UNIFORM_BALL, candidates_positions=EuclideanSpace.UNIFORM_BALL)
#     res, _ = is_DUE(instance)
#     assert res == True or None
    
# print("Testing neagative examples DUE (Prefsampling + added votes)")
# for _ in trange(100):
    # a = random.randint(5, 50)
    # v = random.randint(5, 50)
    # instance = euclidean_vcr(num_voters=v, num_candidates=a, voters_radius=1/a, candidates_radius=1/a, num_dimensions=1, voters_positions=EuclideanSpace.UNIFORM_BALL, candidates_positions=EuclideanSpace.UNIFORM_BALL)
    # vote = {i for i in range(a)}
    # instance.append(vote)
    # for i in range(a):
    #     vote = {i}
    #     instance.append(vote)
    # res, _ = is_DUE(instance)
    # assert res == False or None

# print("Testing positive examples DUE (WSC)")
# for _ in trange(100):
#     a = random.randint(10, 20)
#     alternatives = [i for i in range(a)]
#     v = random.randint(5, len(list(combinations(alternatives, 2))))
#     instance = generate_WSC_instance(a, v)
#     res, _ = is_DUE(instance)
#     assert res == True or None

# print("Testing neagtive examples DUE (WSC)")
# for _ in trange(100):
#     a = random.randint(10, 20)
#     alternatives = [i for i in range(a)]
#     v = random.randint(5, len(list(combinations(alternatives, 2))))
#     instance = generate_NOT_WSC_instance(a, v)
#     res, _ = is_DUE(instance)
#     assert res == False or None

# print("Testing positive examples DUE (CEI)")
# for _ in trange(1):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_CEI_instances(a, v)
#     res, _ = is_DUE(instance)
#     assert res == True

# print("Testing positive examples DUE (VEI)")
# for _ in trange(1):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_VEI_instances(a, v)
#     res, _ = is_DUE(instance)
#     assert res == True

# print("Testing positive examples DUE (PART)")
# for _ in trange(1):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_PART_instances(a, v)
#     res, _ = is_DUE(instance)
#     assert res == True

# # ADD POS DUE WITH PRESAMPLING?

# print("Testing negative examples DUE (not CI)")
# for _ in trange(10):
#     a = random.randint(5, 30)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CI_instances(a, v)
#     res, _ = is_DUE(instance)
#     assert res == False

# print("Testing negative examples DUE (T1)")
# for _ in trange(10):
#     a = random.randint(5, 30)
#     instance = generate_NOT_CI_CEI_instances_T1(a)
#     res, _ = is_DUE(instance)
#     assert res == False

# print("Testing negative examples DUE (T2)")
# for _ in trange(10):
#     a = random.randint(5, 30)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, _ = is_DUE(instance)
#     assert res == False

# print("Testing negative examples DUE (T3)")
# for _ in trange(10):
#     a = random.randint(5, 30)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, _ = is_DUE(instance)
#     assert res == False

# print("Testing negative examples DUE (T4)")
# for _ in trange(1):
#     a = random.randint(5, 30)
#     instance = instance_NOT_CI_CEI_T4
#     res, _ = is_DUE(instance)
#     assert res == False

# print("Testing negative examples DUE (T5)")
# for _ in trange(1):
#     a = random.randint(5, 30)
#     instance = instance_NOT_CI_CEI_T5
#     res, _ = is_DUE(instance)
#     assert res == False