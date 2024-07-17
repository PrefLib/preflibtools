import random


def generate_CI_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Generate 'v' votes
    for _ in range(v):
        # Take a left bound
        left = random.randint(0, a-1)

        # Take a right bound
        right = random.randint(left, a)

        # Create a vote with the alternatives between the left and right bound to make sure it is a interval
        vote = [alternatives[j] for j in range(left, right)]
        instance.append(vote)
    
    return instance

def generate_NOT_CI_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Generate 'v' votes
    for _ in range(v):
        # Take a left bound
        left = random.randint(0, a-1)

        # Take a right bound
        right = random.randint(left, a)

        # Create a vote with the alternatives between the left and right bound to make sure it is a interval
        vote = [alternatives[j] for j in range(left, right)]
        instance.append(vote)
    
    # Create a vote of ervery single alternative and vote with that alterntive with the last one to be sure no CI
    for i in range(len(alternatives)-1):
        vote = [alternatives[i]]
        instance.append(vote)
        vote = [alternatives[i], alternatives[-1]]
        instance.append(vote)

    return instance

def generate_CEI_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Generate 'v' votes
    for _ in range(v):

        # Choose random to create a prefix (0) or a suffcix (1)
        fix = random.randint(0,1)

        # Take a random length for the vote
        length = random.randint(0, a-1)

        # If prefix
        if fix == 0:

            # Create a vote from the most left alternative to length, to make sure interval and prefix
            vote = [alternatives[j] for j in range(0, length)]
            instance.append(vote)
        
        # Else if suffix
        else:

            # Create a vote from length to the last alternative, to make sure interval and suffix
            vote = [alternatives[j] for j in range(length, a)]
            instance.append(vote)

    return instance

def generate_NOT_CEI_instances(a, v):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Initiate the instance
    instance = []

    # Generate 'v' votes
    for _ in range(v):

        # Choose random to create a prefix (0) or a suffcix (1)
        fix = random.randint(0,1)

        # Take a random length for the vote
        length = random.randint(0, a-1)

        # If prefix
        if fix == 0:

            # Create a vote from the most left alternative to length, to make sure interval and prefix
            vote = [alternatives[j] for j in range(0, length)]
            instance.append(vote)
        
        # Else if suffix
        else:

            # Create a vote from length to the last alternative, to make sure interval and suffix
            vote = [alternatives[j] for j in range(length, a)]
            instance.append(vote)

    # Create a vote of ervery single alternative and vote with that alterntive with the last one to be sure no CI
    for i in range(len(alternatives)-1):
        vote = [alternatives[i]]
        instance.append(vote)
        vote = [alternatives[i], alternatives[-1]]
        instance.append(vote)

    return instance

# Generate instance in the form of the Tucker 2 matrix
def generate_NOT_CI_CEI_instances_T1(a):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]
    instance = []

    # Add two alternatives around the diagonal as votes
    for i in range(a-1):
        instance.append([alternatives[i], alternatives[i+1]])

    # Add vote on first and last alter
    instance.append([alternatives[0], alternatives[-1]])

    return instance

# Generate instance in the form of the Tucker 2 matrix
def generate_NOT_CI_CEI_instances_T2(a):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]
    instance = []

    # Add two alternatives around the diagonal as votes
    for i in range(a-2):
        instance.append([alternatives[i], alternatives[i+1]])
    
    # Append all alternatives except the first one
    instance.append(alternatives[1:])

    # Append all alternatives except the second to last
    instance.append(alternatives[:-2] + alternatives[-1:])

    return instance

# Generate instance in the form of the Tucker 3 matrix
def generate_NOT_CI_CEI_instances_T3(a):
    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]
    instance = []

    # Add two alternatives around the diagonal as votes
    for i in range(a-2):
        instance.append([alternatives[i], alternatives[i+1]])
    
    # Append all alternatives except first and the second to last
    instance.append(alternatives[1:-2] + alternatives[-1:])

    return instance

# Instance in the form of a Tucker 4 matrix
instance_NOT_CI_CEI_T4 = [
        ['A', 'B'],
        ['C', 'D'],
        ['E', 'F'],
        ['B', 'D', 'F']
    ]

# Instance in the form of a Tucker 5 matrix
instance_NOT_CI_CEI_T5 =[
    ['A', 'B'],
    ['A', 'B', 'C', 'D'],
    ['C', 'D'],
    ['A', 'D', 'E']
]

def generate_VI_instances(a, v):
    # Generate 'v' voters
    instance = [[] for _ in range(v)]

    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # For every alternative add them to voters that form an interval
    for alt in alternatives:

        # Choose left bound
        left = random.randint(0, v-1)

        # Choose right bound
        right = random.randint(left, v)

        # Append the alternative to all voters in those bounds to make sure is interval
        for voter in range(left, right):
            instance[voter].append(alt)

    return instance

def generate_VEI_instances(a, v):
    # Generate 'v' voters
    instance = [[] for _ in range(v)]

    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # For every alternative add them to voters that form an interval
    for alt in alternatives:

        # Choose random to create a prefix (0) or a suffcix (1)
        fix = random.randint(0, 1)

        # If prefix
        if fix == 0:

            # Make an interval from moest left voter till right bound
            right = random.randint(0, v)

            # Append alternative to all voters starting from first voter to make sure interval and prefix
            for voter in range(0, right):
                instance[voter].append(alt)

        # If suffix
        else:

            # Make an interval from left bound voter till last voter
            left = random.randint(0, v)

            # Append alternative to all voters starting from left bound voter to last voter make sure interval and prefix
            for voter in range(left, v):
                instance[voter].append(alt)

    return instance

# Generate instance in the form of the Tucker 1 matrix
def generate_NOT_VI_VEI_instances_T1(a):
    # Generate 'v' voters
    instance = [[] for _ in range(a)]

    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Add two alternatives around the diagonal to votes
    for i in range(a-1):
        instance[i].append(alternatives[i])
        instance[i+1].append(alternatives[i])
    
    # Add last alternative to first vote 
    instance[0].append(alternatives[-1])

    # Add last alternatiev to last vote
    instance[-1].append(alternatives[-1])

    return instance

# Generate instance in the form of the Tucker 2 matrix
def generate_NOT_VI_VEI_instances_T2(a):
    # Generate 'a' voters
    instance = [[] for _ in range(a)]

    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Add two alternatives around the diagonal to votes
    for i in range(a-2):
        instance[i].append(alternatives[i])
        instance[i+1].append(alternatives[i])

    # Add second to last alternative to all voters except first
    for i in range(1, a):
        instance[i].append(alternatives[-2])

    # Add last alternative to all voters except last (last voter still to be added in next step)
    for i in range(a-2):
        instance[i].append(alternatives[-1])
    
    # Add last voter with last alternative
    instance[-1].append(alternatives[-1])

    # Add vote only on last two alternatives
    instance.append(alternatives[-2:])

    return instance

# Generate instance in the form of the Tucker 3 matrix
def generate_NOT_VI_VEI_instances_T3(a):
    # Generate 'a' voters
    instance = [[] for _ in range(a)]

    # Generate 'a' alternatives
    alternatives = [i+1 for i in range(a)]

    # Add two alternatives around the diagonal to votes
    for i in range(a-1):
        instance[i].append(alternatives[i])
        instance[i+1].append(alternatives[i])

    # Add second to second to last alternative to all voters except first
    for i in range(1, a-2):
        instance[i].append(alternatives[-1])

    # Add a vote with only last alternative
    instance.append(alternatives[-1:])

    return instance

# Instance in the form of the Tucker 4 matrix
instance_NOT_VI_VEI_T4 =[
    ['A'],
    ['A', 'D'],
    ['B'],
    ['B', 'D'],
    ['C'],
    ['C', 'D']
]

# Instance in the form of the Tucker 4 matrix
instance_NOT_VI_VEI_T5 =[
    ['A', 'B', 'D'],
    ['A', 'B'],
    ['B', 'C'],
    ['B', 'C', 'D'],
    ['D']
]

'''
Uncomment to run the tests
'''
  
# print("Testing positive examples CI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_CI_instances(a, v)
#     res, res2 = is_candidate_interval(instance)
#     assert res == True

# print("Testing negative examples CI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CI_instances(a, v)
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing negative examples CI (Tucker 1)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T1(a)
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing negative examples CI (Tucker 2)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T2(a)
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing negative examples CI (Tucker 3)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing negative example CI (Tucker 4)")
# for _ in trange(1):
#     instance = instance_NOT_CI_CEI_T4
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing negative example CI (Tucker 5)")
# for _ in trange(1):
#     instance = instance_NOT_CI_CEI_T5
#     res, res2 = is_candidate_interval(instance)
#     assert res == False

# print("Testing positive examples CEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_CEI_instances(a, v)
#     res, _ = is_candidate_extremal_interval(instance)
#     assert res == True
    
# print("Testing negative examples CEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CEI_instances(a, v)
#     res, _ = is_candidate_extremal_interval(instance)
#     assert res == False
    
# print("Testing negative examples CEI (Tucker 1)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T1(a)
#     res, res2 = is_candidate_extremal_interval(instance)
#     assert res == False

# print("Testing negative examples CEI (Tucker 2)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T2(a)
#     res, res2 = is_candidate_extremal_interval(instance)
#     assert res == False
    
# print("Testing negative examples CEI (Tucker 3)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_CI_CEI_instances_T3(a)
#     res, res2 = is_candidate_extremal_interval(instance)
#     assert res == False

# print("Testing negative example CEI (Tucker 4)")
# for _ in trange(1):
#     instance = instance_NOT_CI_CEI_T4
#     res, res2 = is_candidate_extremal_interval(instance)
#     assert res == False

# print("Testing negative example CEI (Tucker 5)")
# for _ in trange(1):
#     instance = instance_NOT_CI_CEI_T5
#     res, res2 = is_candidate_extremal_interval(instance)
#     assert res == False

# print("Testing positive examples VI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_VI_instances(a, v)
#     res, _ = is_voter_interval(instance)
#     assert res == True

# print("Testing negative examples VI (Tucker 1)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T1(a)
#     res, _ = is_voter_interval(instance)
#     assert res == False

# print("Testing negative examples VI (Tucker 2)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T2(a)
#     res, _ = is_voter_interval(instance)
#     assert res == False
    
# print("Testing negative examples VI (Tucker 3)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T3(a)
#     res, _ = is_voter_interval(instance)
#     assert res == False

# print("Testing negative example VI (Tucker 4)")
# for _ in trange(1):
#     instance = instance_NOT_VI_VEI_T4
#     res, _ = is_voter_interval(instance)
#     assert res == False

# print("Testing negative example VI (Tucker 5)")
# for _ in trange(1):
#     instance = instance_NOT_VI_VEI_T5
#     res, _ = is_voter_interval(instance)
#     assert res == False

# print("Testing postive examples VEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_VEI_instances(a, v)
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == True

# print("Testing negative examples VEI (Tucker 1)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T1(a)
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == False
    
# print("Testing negative examples VEI (Tucker 2)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T2(a)
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == False

# print("Testing negative examples VEI (Tucker 3)")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     instance = generate_NOT_VI_VEI_instances_T3(a)
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == False

# print("Testing negative example VEI (Tucker 4)")
# for _ in trange(1):
#     instance = instance_NOT_VI_VEI_T4
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == False

# print("Testing negative example VEI (Tucker 5)")
# for _ in trange(1):
#     instance = instance_NOT_VI_VEI_T5
#     res, _ = is_voter_extremal_interval(instance)
#     assert res == False