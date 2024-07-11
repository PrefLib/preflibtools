from preflibtools.instances import OrdinalInstance
from prefsampling.ordinal import singlepeaked


import numpy as np

def generate_k_alt_nearly_sp(num_voters, num_alternatives, k, seed = None):
    """Generates a non-single-peaked profile that becomes single-peaked after
    k alternatives are deleted. This is done by generating a single-peaked profile and
    adding extra orders such that there remain WD-structures untill k alternatives are removed.

    :param num_voters: Number of orders to sample.
    :type num_voters: int
    :param num_alternatives: Number of alternatives
    :type num_alternatives: int
    :param k: Number of alternatives that violate single-peakedness.
    :type k: int
    :param seed: Seed for numpy random number generator
    :type seed: int

    :return: 
    :rtype: list(list)
    """
    if num_voters < (2 + k):
        raise ValueError(
            f"Must need at least {2+k} votes for {k}-alternative deletion"
        )
    
    if k > num_alternatives:
        raise ValueError(
            "Cannot remove more alternatives than total."
        )
    
    rng = np.random.default_rng(seed)

    votes = singlepeaked.single_peaked_walsh(num_voters - (2+k), num_alternatives, seed=seed)
    axis = [i for i in range(num_alternatives)]

    votes.append(axis)
    votes.append(list(reversed(axis)))

    alternatives_to_remove = rng.choice(axis[1:-1], k, replace=False)

    for alt in alternatives_to_remove:
        new_vote = [a for a in axis if a != alt]
        new_vote.append(alt)
        votes.append(new_vote)

    return votes

#########################################################################################

def remove_alternatives(profile, violating_alternatives):
    """Removes a set of single-peakedness violating alternatives from a given profile.

    :param profile: Instance to remove the given alternatives from.
    :type profile: preflibtools.instances.preflibinstance.OrdinalInstance
    :param violating_alternatives: Alternatives to remove from the orders in the profile.
    :type violating_alternatives: list

    :return: A new profile containing the orders of the given profile without the given alternatives
    removed.
    :rtype: preflibtools.instances.preflibinstance.OrdinalInstance
    """
    old_votes = profile.full_profile()
    
    new_num_alternatives = profile.num_alternatives - len(violating_alternatives)
    new_votes = np.zeros([len(old_votes), new_num_alternatives], dtype = int)

    for i, vote in enumerate(old_votes):
        m = 0

        for c in vote:
            c = c[0]

            if c not in violating_alternatives:
                new_votes[i][m] = c
                m += 1
    
    instance = OrdinalInstance()
    instance.append_order_array(new_votes)
    return instance

#########################################################################################

def k_alternative_deletion(instance):
    """Generates the longest incomplete axis on which the given profile does
    not violate single-peakedness, thereby identifying the minimum number
    of alternatives that should be deleted in order for it to become single-peaked.

    This function utilizes the algorithm of Erdélyi, Lackner, Pfandler (2017).

    :param instance: the instance to test for k-alternative deletion single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: The longest incomplete axis on which the given instance is single-peaked,
    as well the alternatives missing from said axis that would need to be removed from the profile.
    :rtype: Tuple(list, list)
    """
    alternatives = list(instance.alternatives_name.keys())

    longest_axis, remove_alternatives = longest_single_peaked_axis(instance, alternatives)

    return longest_axis, remove_alternatives


def longest_single_peaked_axis(instance, alternatives):
    """Generates the longest incomplete axis on which the given profile does
    not violate single-peakedness, thereby identifying the minimum number
    of alternatives that should be deleted in order for it to become single-peaked.

    This function implements the algorithm of Erdélyi, Lackner, Pfandler (2017).

    :param instance: the instance to test for k-alternative deletion single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param alternatives: the (sub)set of alternatives to apply the algorithm on.
    :type alternatives: list

    :return: The longest incomplete axis on which the given instance is single-peaked,
    as well the alternatives missing from said axis that would need to be removed from the profile.
    :rtype: Tuple(list, list)
    """
    m = len(alternatives)
    remaining_alternatives = alternatives
    unique_votes = [vote for vote, _ in instance.flatten_strict()]

    # Construct L sets
    L = get_L_sets(alternatives, unique_votes)

    # Construct S dict
    S = {
        0 : {
            ((None, None, None, None), frozenset()): [None]
        }
    }

    # Keep track of axes that can't be extended (case 3 of place function)
    locked_axis = [None]

    # Keep track of longest constructed axis
    longest = [None]

    for i in range(1, m+1):
        S[i] = dict(S[i-1])

        for key in S[i-1]:
            A = S[i-1][key]

            if None not in A:
                continue
                
            # No need to bother if current axis can't exceed longest found with remaining alternatives
            if len(A) + len(remaining_alternatives) < len(longest):
                continue

            extensions = N(i, m, key[-1], L, unique_votes)

            for X in extensions:
                new_A, consistent = place(A, X, unique_votes)

                if consistent:
                    
                    if len(new_A) > len(longest):
                        longest = new_A

                    new_key = (boundary(new_A), X)
                    
                    if new_key not in S[i]:
                        S[i][new_key] = new_A
                    elif len(new_A) > len(S[i][new_key]):
                        S[i][new_key] = new_A
                
                # Keep track of longest locked axis
                elif new_A != A and len(new_A) > len(locked_axis):
                    locked_axis = new_A

        remaining_alternatives = [c for c in remaining_alternatives if c not in L[i]]

    if len(locked_axis) > len(longest):
        longest = locked_axis

    longest.remove(None)
    removed_alternatives = [i for i in alternatives if i not in longest ] 

    return longest, removed_alternatives


def get_L_sets(alternatives, unique_votes):
    """A helper function for the k-alternative deletion algorithm.
    Generates the set of sets of alternatives, based on what their lowest rank
    is among all votes. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param alternatives: The (sub)set of alternatives to apply the algorithm on.
    :type alternatives: list.
    :param unique_votes: The unique orders within the profile.
    :type unique_votes: list(list)

    :return: A dictionary of sets, such that the i-th set contains the alternatives placed last
    after i-1 last placed alternative removals.
    :rtype: dict(set)
    """
    L = dict()
    m = len(alternatives)

    votes_copy = list(unique_votes)
    previous_last = set()
    last = set()

    for j in range(1, m+1):
        for i in range(len(votes_copy)):
            new_order = [a for a in votes_copy[i] if a not in previous_last and a in alternatives]

            if len(new_order) > 0:
                last.add(new_order[-1])
            votes_copy[i] = new_order
        
        L[j] = last
        previous_last = last
        last = set()
    
    return L


def N(i, m, Y, L, unique_votes):
    """A helper function for the k-alternative deletion algorithm.
    Generates the set of sets of alternatives that are eligable to be placed at
    this step of the procedure. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param i: iteration of the k-alternative deletion algorithm.
    :type i: int
    :param m: number of alternatives.
    :type m: int
    :param Y: Previous alternatives placed on the current axis.
    :type Y: set
    :param L: L sets, ordering the alternatives based on their lowest-rank.
    :type L: dict(set)
    :param unique_votes: The unique orders within the profile.
    :type unique_votes: list(list)

    :return: set of pairs or singletons of alternatives eligable to be placed next on
    the axis.
    :rtype: set(set)
    """
    remaining_alternatives = L[i].copy()

    for pos in range(i, m):
        remaining_alternatives.update(L[pos])

    X = {frozenset([x_1, x_2]) for x_1 in L[i] for x_2 in remaining_alternatives if Last_check(unique_votes, Y, [x_1, x_2])}
    return X

def Last_check(unique_votes, previous_alternatives, alternatives):
    """A helper function for the k-alternative deletion algorithm.
    Do not place a set of new alternatives if one of said alternatives is always ranked higher
    than the rest. Do not place a set of new alternatives if there is a vote that ranks one lower
    than the previously placed alternatives.
    """

    restriction = []
    restriction.extend(alternatives)
    restriction.extend(previous_alternatives)

    last_of_all_alt = set()
    last_of_new_alt = set()

    for i in range(len(unique_votes)):
        full_restricted_vote = [a for a in unique_votes[i] if a in restriction]
        new_alt_restricted_vote = [a for a in full_restricted_vote if a in alternatives]

        last_of_all_alt.add(full_restricted_vote[-1])
        last_of_new_alt.add(new_alt_restricted_vote[-1])
    
    previous_are_last = True
    both_new_are_last = True
    for alt in alternatives:
        if alt in last_of_all_alt and len(previous_alternatives) != 0:
            previous_are_last = False
        
        if alt not in last_of_new_alt:
            both_new_are_last = False
    
    return previous_are_last and both_new_are_last


def place(axis, X, votes):
    """A helper function for the k-alternative deletion algorithm.
    Places a set of alternatives on the given axis if that would not violate
    single-peakedness given the votes. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param axis: axis to place the new alternatives on.
    :type axis: list
    :param X: new alternatives to be placed.
    :type X: set
    :param votes: unique votes of the profile.
    :type votes: list[list]
    """
    new_axis = list(axis)
    if len(X) > 2:
        return new_axis, False

    if len(X) == 1:
        return case_3(new_axis, X, votes)
    
    if len(X) == 2:
        return case_2(new_axis, X, votes)


def case_2(axis, X, votes):
    """A helper function for the k-alternative deletion algorithm.
    Case 2 of place function. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param axis: axis to place the new alternatives on.
    :type axis: list
    :param X: the two new alternatives to be placed.
    :type X: set
    :param votes: unique votes of the profile.
    :type votes: list[list]

    :return: The resulting axis and whether more alternatives can be placed on this
    new axis (if it remains single-peaked).
    :rtype: tuple(list, bool)
    """
    x1, x2 = list(X)[0], list(X)[1]
    bound = boundary(axis)

    flag_c1, flag_d1 = False, False
    flag_c2, flag_d2 = False, False

    if (bound[1] is not None
        or bound[2] is not None):

        for vote in votes:
            id_x1 = vote.index(x1)
            id_x2 = vote.index(x2)

            b = [vote.index(b_i) if b_i is not None else None for b_i in bound]

            if (b[1] is not None and b[2] is not None):
                if ((b[1] < id_x1 and b[2] < id_x1)
                    or (b[1] < id_x2 and b[2] < id_x2)):
                    return axis, False
            
            if (b[0] is not None or b[3] is not None):
                if check_case_4(b, id_x1) or check_case_4(b, id_x2):
                    return axis, False
                
            if b[2] is not None:
                if (b[2] < id_x1 and id_x2 < id_x1):
                    flag_c1 = True

                if (b[2] < id_x2 and id_x1 < id_x2):
                    flag_c2 = True

            if b[1] is not None:
                if (b[1] < id_x1 and id_x2 < id_x1):
                    flag_d1 = True

                if (b[1] < id_x2 and id_x1 < id_x2):
                    flag_d2 = True
            
            if ((flag_c1 and flag_d1)
                or (flag_c2 and flag_d2)
                or (flag_c1 and flag_c2)
                or (flag_d1 and flag_d2)):
                return axis, False
            
    id_none = axis.index(None)
    first_half, second_half = axis[:id_none], axis[id_none+1:]

    if (flag_c2 or flag_d1):
        first_half.append(x2)
        second_half.insert(0, x1)
    else:
        first_half.append(x1)
        second_half.insert(0, x2)

    axis = first_half + [None] + second_half
    return axis, True


def case_3(axis, X, votes):
    """A helper function for the k-alternative deletion algorithm.
    Case 3 of place function. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param axis: axis to place the new alternatives on.
    :type axis: list
    :param X: the new alternative to be placed.
    :type X: set
    :param votes: unique votes of the profile.
    :type votes: list[list]

    :return: The resulting axis and whether more alternatives can be placed on this
    new axis (if it remains single-peaked).
    :rtype: tuple(list, bool)   
    """
    x = list(X)[0]

    bound = boundary(axis)

    flag_c, flag_d = False, False

    if (bound[1] is not None
        or bound[2] is not None):

        for vote in votes:
            id_x = vote.index(x)

            b = [vote.index(b_i) if b_i is not None else None for b_i in bound]

            if (b[1] is not None and b[2] is not None):
                if (b[1] < id_x and b[2] < id_x):
                    return axis, False
            
            if (b[0] is not None or b[3] is not None):
                if check_case_4(b, id_x):
                    return axis, False
            
            if b[2] is not None:
                if b[2] < id_x:
                    flag_c = True
            
            if b[1] is not None:
                if b[1] < id_x:
                    flag_d = True
                        
    id_x = axis.index(None)
    if flag_d:
        id_x += 1
    
    axis.insert(id_x, x)

    return axis, not (flag_c and flag_d)


def check_case_4(b, x):
    """A helper function for the k-alternative deletion algorithm.
    Case 4 of place function. See Erdélyi, Lackner, Pfandler (2017) for details.

    :param b: boundary of the current axis in the place function.
    :type b: list
    :param x: a vote's ranking of one of the alternatives being placed.
    :type x : int

    :return: whether this alternative violates case 4 of the place function.
    :rtype: bool
    """
    left_b, right_b = False, False

    if b[0] is not None and b[1] is not None:
        left_b = b[0] < b[1] and x < b[1]

    if b[3] is not None and b[2] is not None:
        right_b = b[3] < b[2] and x < b[2]

    return left_b or right_b


def boundary(axis):
    """A helper function for the k-alternative deletion algorithm.
    Given an incomplete axis, returns the boundary identifier.
    See Erdélyi, Lackner, Pfandler (2017) for details.

    :param axis: (incomplete) axis of alternatives.
    :type axis: list

    :return: boundary identifier of this axis.
    :rtype: tuple
    """
    if None not in axis:
        return
    
    x = axis.index(None) + 2
    tmp = [None, None] + axis + [None, None]
    ids = [x - 2, x - 1, x + 1, x + 2]
    
    return tuple([tmp[i] for i in ids])

#########################################################################################