from itertools import combinations

def is_2partition(instance):
    # Create a set of all possible alternatives
    alternatives = set().union(*instance)

    # Create all possible sizes for the combinations
    for s in range(1, len(instance)):

        # Create and loop over all combinations of instances of size s and use index
        for part1_idx in combinations(range(len(instance)), s):

            # Create the partitions from combinations 
            part1 = set().union(*(instance[idx] for idx in part1_idx))
            part2 = alternatives - part1

            # Check for every vote if its either a subset of part1 or part2
            if all(vote <= part1 or vote <= part2 for vote in instance):
                print(f"Partition 1 = {part1} and Partition 2 = {part2}")
                return True
                
    return False


# Example data
instance = [
    {'A', 'B'},  # Voter 1 chooses candidates A and B
    {'C'},       # Voter 2 chooses candidate C
    {'D', 'E'},  # Voter 3 chooses candidates D and E
    {'A', 'C'}   # Voter 4 chooses candidates A and C
]

# Check if the data is 2-partition
result = is_2partition(instance)
print("Is the data 2-partition?:", result)

