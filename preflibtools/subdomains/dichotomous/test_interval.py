from interval import *
from tqdm import trange
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

def generate_NOT_VI_instances(a, v):
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
        
    # TODO!

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

def generate_NOT_VEI_instances(a, v):
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

    #TODO!

    return instance

# print("Testing positive examples CI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_CI_instances(a, v)
#     res, res2 = is_CI(instance)
#     assert res == True

# print("Testing negative examples CI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CI_instances(a, v)
#     res, res2 = is_CI(instance)
#     assert res == False

# print("Testing positive examples CEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_CEI_instances(a, v)
#     res, _ = is_CEI(instance)
#     assert res == True
    
# print("Testing negative examples CEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_CEI_instances(a, v)
#     res, _ = is_CEI(instance)
#     assert res == False

# print("Testing positive examples VI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_VI_instances(a, v)
#     res, _ = is_VI(instance)
#     assert res == True

# print("Testing negative examples VI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_VI_instances(a, v)
#     res, _ = is_VI(instance)
#     assert res == False

# print("Testing negative examples VEI")
# for _ in trange(1000):
#     a = random.randint(5, 100)
#     v = random.randint(5, 100)
#     instance = generate_NOT_VEI_instances(a, v)
#     res, _ = is_VEI(instance)
#     assert res == True