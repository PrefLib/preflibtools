from interval import is_candidate_interval
from mip import Model, minimize, BINARY, CONTINUOUS, OptimizationStatus, SearchEmphasis


def is_dichotomous_euclidean(instance):
    res, (order, _) = is_candidate_interval(instance)

    if not res:
        return False, None

    # Place all alternatives over a line
    alternative_positions = [(alt, pos) for pos, alt in enumerate(order)]
    voter_position_radius = []

    # Check for every vote
    for vote in range(len(instance)):
        left = None
        right = None
        voter = f'V{vote+1}'

        # Empty votes have no position or radius
        if len(instance[vote]) == 0:
            voter_position_radius.append((voter, None, None))

        # Votes with one alternative get that postion of the alternative and radius zero
        elif len(instance[vote]) == 1:
            index = order.index(instance[vote][0])
            voter_position_radius.append((voter, 0, index))

        elif len(instance[vote]) > 1:

            # Check for every alternative of the vote the index and keep track of the lowest (left) and greatest (right) index
            for alt in instance[vote]:
                index = order.index(alt)

                if left is None or index < left:
                    left = index
                if right is None or index > right:
                    right = index

            # The position of the voter will be in the middle of the alternatives and the radius is that by half
            radius = (right - left) / 2
            position = (left + right) / 2
            voter_position_radius.append((voter, position, radius))

    # Return tuple of the voters with position and radius and tuple with the alternative postitions
    return True, (voter_position_radius, alternative_positions)


def is_possibly_euclidean(instance):
    res, _ = is_candidate_interval(instance)
    return res, None


def _check_DUE(m, voter_vars, alt, r, instance, start_idx, end_idx):
    alternatives = sorted(set().union(*instance))
    num_alt = len(alternatives)

    # Init M for big_M method and epsilon
    M = num_alt + 1
    epsilon = 1e-3

    for i in range(start_idx, end_idx):
        # Take the vote and create a new variable for the voter and add to list
        vote = instance[i]
        voter = m.add_var(name=f"V_{i}", var_type=CONTINUOUS, lb=0, ub=1)
        voter_vars.append(voter)

        for a in alternatives:
            j = alternatives.index(a)

            # Constraint if alternative in vote
            if a in vote:

                # Constraint: |p(i) - p(c)| <= r
                m += voter - alt[j] <= r
                m += alt[j] - voter <= r

            # Constraint if alternative not in vote
            else:

                # Constraint: |p(i) - p(c)| > r
                z = m.add_var(var_type=BINARY)

                # Use variable z to make '>' work
                m += voter - alt[j] >= r + epsilon - M * z
                m += alt[j] - voter >= r + epsilon - M * (1 - z)

    
# Check Dichotomous Uniformly Euclidean
def is_dichotomous_uniformly_euclidean(instance_input, time_limit=300):
    num_voters = len(instance)
    alternatives = sorted(set().union(*instance))
    num_alt = len(alternatives)

    # Init model
    m = Model()

    # Make model look for feasible solution instead of optimal
    m.emphasis = SearchEmphasis.FEASIBILITY

    # Create a variable for every alternative and list to add variables for voters
    alt = [m.add_var(name=f"A_{j}", var_type=CONTINUOUS, lb=0, ub=1) for j in range(num_alt)]
    voter_vars = []

    # Create variable for radius
    r = m.add_var(name="r", var_type=CONTINUOUS, lb=0, ub=1)

    # Set objective
    m.objective = minimize(r)

    # Set to 0 to not print progress
    m.verbose = 0

    # Step size to check batch of voters if satisfies DUE
    step = 10

    # start index and end index to check DUE in batches
    for start_idx in range(0, num_voters, step):
        end_idx = min(start_idx + step, num_voters)

        # Check DUE by addinf the variables for voters and contraints for that batch
        _check_DUE(m, voter_vars, alt, r, instance, start_idx, end_idx)
        
        # Optimize model
        status = m.optimize(max_solutions=1, max_seconds=time_limit)

        # Check if solution was found, is so continue otherwise stop and return False
        if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
            continue

        # If problem take too long to solve based on time limit, there is no solution
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print("No solution found in time limit")
            return None, ([], [], None)
        
        else:
            return False, ([], [], None)

    # Check if solution was found after all iterations
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:

        # Get values for voters and alternatives
        voter_pos = [(f"V_{i+1}", voter_vars[i].x) for i in range(num_voters)]
        alt_pos = [(alternatives[i], alt[i].x) for i in range(num_alt)]

        # Add slightly smaller value than epsilon to radius
        radius = r.x + 0.9e-3

        return True, (voter_pos, alt_pos, radius)
    else:
        return False, ([], [], None)