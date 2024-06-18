from partition import *
import random
from tqdm import trange

'''
Use for testing of functions in partition.py
'''

# Example data
instance = [
    {'A', 'B'},  # Voter 1 chooses alternatives A and B
    {'C'},       # Voter 2 chooses alternative C
    {'D', 'E'},  # Voter 3 chooses alternatives D and E
    {'A', 'C'}   # Voter 4 chooses alternatives A and C
]

# TEST 1
# Check if recognizing 2part. Also is_partitioning should find the 2part
instance1 = [
    {'A', 'B'},
    {'C'}
]

# Make sure both find partitions and return True
assert is_2PART(instance1)[0] == True
assert is_PART(instance1)[0] == True

# Check if they both return the same partition in this case
assert is_2PART(instance1)[1] == is_PART(instance1)[1]

# TEST 2
# Check if correct output with only one voter
instance2 = [
    {'A'}
]

assert is_2PART(instance2)[0] == False
assert is_PART(instance2)[0] == True

# TEST 3
# Check if handles empty votes
instance3 =[
    {}
]

assert is_2PART(instance3)[0] == False
assert is_PART(instance3)[0] == False

# TEST 4

def generate_2PART_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Generate a random cut to cut the alternative list into 2 groups of at least length 1
    cut = random.randint(1, a-1)

    # Votes devided by two because for every v, two votes will be appended
    v = v // 2

    # Generate 'v' votes
    for _ in range(v):

        # Create a votes with the alternatives split in 2 groups
        vote = [alternatives[j] for j in range(0, cut)]
        instance.append(vote)
        vote = [alternatives[j] for j in range(cut, a)]
        instance.append(vote)

    return instance

def generate_NOT_2PART_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []
    # Generate a random cut to cut the alternative list into 2 groups of at least length 1
    cut = random.randint(1, a-1)

    # Votes devided by two because for every v, two votes will be appended
    v = v // 2

    # Generate 'v' votes
    for _ in range(v):

        # Create a votes with the alternatives split in 2 groups
        vote = [alternatives[j] for j in range(0, cut)]
        instance.append(vote)
        vote = [alternatives[j] for j in range(cut, a)]
        instance.append(vote)

    # Add one wrong vote by adding a vote with two alternatives that are certainly not in same part
    instance.append([alternatives[0], alternatives[-1]])
    return instance

def generate_PART_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Determine randomly the number of partitions created, at least 2
    partitions = random.randint(2, a)

    # Determine randomly the indices of where to partition
    partition_indices = sorted(random.sample(range(1, a), partitions-1))

    # Votes devided by paritions because for every v, num of partition votes will be appended
    v = v // partitions 

    for _ in range(v):
        # Keep track of previous index for the next partition
        prev_index = 0 

        # Partition on all the indices
        for partition_index in partition_indices:

            # Create a vote of the partition
            vote = [alternatives[j] for j in range(prev_index, partition_index)]
            instance.append(vote)

            # The now the previoud index will be the current one for the next partiton
            prev_index = partition_index

        # Add last partition as vote
        vote = [alternatives[j] for j in range(prev_index, a)]
        instance.append(vote)

    return instance

def generate_NOT_PART_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Determine randomly the number of partitions created, at least 2
    partitions = random.randint(2, a)

    # Determine randomly the indices of where to partition
    partition_indices = sorted(random.sample(range(1, a), partitions-1))

    for _ in range(v):
        # Keep track of previous index for the next partition
        prev_index = 0 

        # Partition on all the indices
        for partition_index in partition_indices:

            # Create a vote of the partition
            vote = [alternatives[j] for j in range(prev_index, partition_index)]
            instance.append(vote)

            # The now the previoud index will be the current one for the next partiton
            prev_index = partition_index

        # Add last partition as vote
        vote = [alternatives[j] for j in range(prev_index, a)]
        instance.append(vote)

    # Add one wrong vote by adding a vote with two alternatives that are certainly not in same part
    instance.append([alternatives[0], alternatives[-1]])

    return instance

# print("Testing positive examples 2PART (for 2PART and PART)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_2PART_instances(a, v)
#     res, _ = is_2PART(instance)
#     res2, _ = is_PART(instance)
#     assert res == True
#     assert res2 == True

# print("Testing negative examples 2PART")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_2PART_instances(a, v)
#     res, _ = is_2PART(instance)
#     res2, _ = is_PART(instance)
#     assert res == False
#     assert res2 == False


# print("Testing positive examples PART")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_PART_instances(a, v)
#     res, _ = is_PART(instance)
#     assert res == True
    
# print("Testing negative examples PART")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_PART_instances(a, v)
#     res, _ = is_PART(instance)
#     assert res == False