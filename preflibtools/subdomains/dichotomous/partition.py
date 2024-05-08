from itertools import combinations

def is_2partition(instance):
    # Create a set of all possible alternatives (WAAR OP GESTEMD IS)!!!!!!!
    alternatives = set().union(*instance)

    # Create all possible sizes for the combinations
    for s in range(1, len(instance)):

        # Create and loop over all combinations of instances of size s and use index
        for part1_idx in combinations(range(len(instance)), s):

            # Create the partitions from combinations 
            part1 = set().union(*(instance[idx] for idx in part1_idx))
            part2 = alternatives - part1

            # Check if both not empty sets
            if part1 and part2:

                # Check for every vote if its either a subset of part1 or part2
                if all(vote <= part1 or vote <= part2 for vote in instance): 
                    print(f"Partition 1 = {part1} and Partition 2 = {part2}")
                    return True
                
    return False

def is_partition(instance):
    # Create list to save partitions
    part = []

    # Pick a vote ffrom instance
    for vote1 in instance:
        # Get the the alternatives from vote
        alternatives = set().union(*vote1)

        # Check for every alternative from vote if found in another vote
        for alt in alternatives:
            for vote2 in instance:
                if alt in vote2:

                    # If alternative found in another vote the rest of the vote must be the same
                    if vote1 != vote2:
                        return False
                    
        # If passed this is a possible partition so add to list              
        part.append(alt)

    print(part)
    return True
