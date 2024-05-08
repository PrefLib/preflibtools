from partition import *

'''
Use for testing of functions in partition.py
'''

# Example data
instance = [
    {'A', 'B'},  # Voter 1 chooses candidates A and B
    {'C'},       # Voter 2 chooses candidate C
    {'D', 'E'},  # Voter 3 chooses candidates D and E
    {'A', 'C'}   # Voter 4 chooses candidates A and C
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