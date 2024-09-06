from preflibtools.properties.subdomains.dichotomous.interval import is_candidate_interval


def is_dichotomous_euclidean(instance):
    """
    Tests whether the given categorical instance representing dichotomous preferences is Euclidean.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is Euclidean, a dictionary mapping voters to
        their position and radius, and a dictionnary mapping alternatives to their position (or None if the instance is
        not Euclidean).
    :rtype: tuple[bool, list | None, list | None]
    """
    res, order = is_candidate_interval(instance)
    if not res:
        return False, None
    alternative_positions = {alt: pos for pos, alt in enumerate(order)}
    voter_position_radius = {}
    for i, ballot in enumerate(instance.preferences):
        approved = ballot[0]
        if len(approved) == 0:
            voter_position_radius[i] = (-1, 0)
        elif len(approved) == 1:
            voter_position_radius[i] = (alternative_positions[approved[0]], 0)
        else:
            left_alt = None
            right_alt = None
            for alt in approved:
                position = alternative_positions[alt]
                if left_alt is None or position < left_alt:
                    left_alt = position
                if right_alt is None or position > right_alt:
                    right_alt = position

            radius = (right_alt - left_alt) / 2
            position = (left_alt + right_alt) / 2
            voter_position_radius[i] = (position, radius)
    return True, (voter_position_radius, alternative_positions)
