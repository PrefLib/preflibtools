from itertools import combinations

def is_2PART(instance):
    # Create list to save partitions
    partition = []

    # Pick a vote ffrom instance
    for vote1 in instance:
        # Get the the alternatives from vote
        alternatives = sorted(list(vote1))

        # Check for every alternative from vote if found in another vote
        for alt in alternatives:
            for vote2 in instance:
                if alt in vote2:

                    # If alternative found in another vote the rest of the vote must be the same
                    if vote1 != vote2:
                        return False, []
        
        # Check if same vote not already added
        if vote1 not in partition:

            # If passed this is a possible partition so add to list              
            partition.append(vote1)

    for part in partition:
        if not part:
            return False, []

    # Must be 2 partitions to be 2PART
    if len(partition) == 2:
        return True, partition
    else:
        return False, []



def is_PART(instance):
    # Create list to save partitions
    partition = []
    # Pick a vote ffrom instance
    for vote1 in instance:
        # Get the the alternatives from vote
        alternatives = sorted(list(vote1))

        # Check for every alternative from vote if found in another vote
        for alt in alternatives:
            for vote2 in instance:
                if alt in vote2:

                    # If alternative found in another vote the rest of the vote must be the same
                    if vote1 != vote2:
                        return False, []
                    
        # Check if same vote not already added
        if vote1 not in partition:

            # If passed this is a possible partition so add to list              
            partition.append(vote1)

    
    for part in partition:
        if not part:
            return False, []

    return True, partition