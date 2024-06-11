from interval import is_CI
from mip import Model, minimize, maximize, BINARY, CONTINUOUS, OptimizationStatus, ConstrList, SearchEmphasis
import random
from test_interval import generate_CEI_instances
import time
from tqdm import trange

# Check Dichotomous Euclidean
def is_DE(instance):
    res, (order, _) = is_CI(instance)

    if res is True:
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
    else:
        return False, None

# Check Possible Euclidean
def is_PE(instance):
    res, _ = is_CI(instance)

    if res is True:
        return True, None
    else:
        return False, None
    
# Check Dichotomous Uniformly Euclidean
def is_DUE(instance):
    num_voters = len(instance)
    alternatives = sorted(set().union(*instance))
    num_alt = len(alternatives)

    # Init model
    m = Model()

    # Make model look for feasible solution instead of optimal
    m.emphasis = SearchEmphasis.FEASIBILITY

    # Create a variable for every voter and every alternative
    voter = [m.add_var(name=f"V_{i}", var_type=CONTINUOUS, lb=0, ub=1) for i in range(num_voters)]
    alt = [m.add_var(name=f"A_{j}", var_type=CONTINUOUS, lb=0, ub=1) for j in range(num_alt)]

    # Create variable for radius
    r = m.add_var(name="r", var_type=CONTINUOUS, lb=0, ub=1)

    # Init M for big_M method and epsilon
    M = num_alt + 1
    epsilon = 1e-3

    # Make constraints for all pairs of voters and alternative depending on vote
    for i, vote in enumerate(instance):
        for a in alternatives:
            j = alternatives.index(a)

            # Constraint if alternative in vote
            if a in vote:

                # Constraint: |p(i) - p(c)| <= r
                m += voter[i] - alt[j] <= r
                m += alt[j] - voter[i] <= r

            # Constraint if alternative not in vote
            else:

                # Constraint: |p(i) - p(c)| > r
                z = m.add_var(var_type=BINARY)

                # Use variable z to make '>' work
                m += voter[i] - alt[j] >= r + epsilon - M * z
                m += alt[j] - voter[i] >= r + epsilon - M * (1 - z)
    
    # Set objective
    m.objective = minimize(r)

    # Optimize model and get status
    status = m.optimize(max_solutions=1)
    print("STATUS:", status)

    # Check if solution was found
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:

        # Get values for voters and alternatives
        voter_pos = [(f"V_{i+1}", voter[i].x) for i in range(num_voters)]
        alt_pos = [(alternatives[i], alt[i].x) for i in range(num_alt)]

        # Add smaller value than epsilon to radius
        radius = r.x + 0.9e-3

        return True, (voter_pos, alt_pos, radius)
    else:
        return False, ([], [], None)


instance = [
    {'A', 'D', 'E', 'F'},
    {'C', 'D'},
    {'A', 'D'},
    {'B', 'C'}
]

res, (voter_pos, alt_pos, radius) = is_DUE(instance)
if res:
    print("Voter postitions:", voter_pos)
    print("Alternative positions:", alt_pos)
    print("R:", radius)

    for voter in voter_pos:
        print("----")
        for alt in alt_pos:
            print(abs(voter[1] - alt[1]) <= radius)

print("Testing positive examples CEI")
for _ in trange(1):
    a = random.randint(999,1000)
    v = random.randint(999,1000)
    instance = generate_CEI_instances(a, v)
    # print(instance)
    start = time.time()
    res, _ = is_DUE(instance)
    end = time.time()
    print("time:", (end-start))
    assert res == True