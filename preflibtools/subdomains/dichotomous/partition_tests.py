from partition import *


# Example data
instance = [
    {'A', 'B'},  # Voter 1 chooses candidates A and B
    {'C'},       # Voter 2 chooses candidate C
    {'D', 'E'},  # Voter 3 chooses candidates D and E
    {'A', 'C'}   # Voter 4 chooses candidates A and C
]

print(is_2partition(instance))