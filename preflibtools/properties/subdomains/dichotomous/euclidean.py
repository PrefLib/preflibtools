from preflibtools.properties.subdomains.dichotomous.interval import is_candidate_interval


def is_dichotomous_euclidean(instance):
    """
    Tests whether the given categorical instance representing dichotomous preferences is Euclidean.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is Euclidean, and the
    positions of the voters and of the candidates (or None if the instance is not Euclidean).
    :rtype: tuple[bool, list | None, list | None]
    """
    res, order  = is_candidate_interval(instance)
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
