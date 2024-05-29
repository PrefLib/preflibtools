from partition import *

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
assert is_2partition(instance1)[0] == True
assert is_partition(instance1)[0] == True

# Check if they both return the same partition in this case
assert is_2partition(instance1)[1] == is_partition(instance1)[1]

# TEST 2
# Check if correct output with only one voter
instance2 = [
    {'A'}
]

assert is_2partition(instance2)[0] == False
assert is_partition(instance2)[0] == True

# TEST 3
# Check if handles empty votes
instance3 =[
    {}
]

assert is_2partition(instance3)[0] == False
assert is_2partition(instance3)[0] == False

# TEST 4
