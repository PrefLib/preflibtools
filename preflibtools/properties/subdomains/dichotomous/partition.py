def is_part(instance):
    """
    Tests whether the given categorical instance is part of the partition subdomain.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is partition and a
        partition of the candidates into sets (or None if the instance is not partition).
    :rtype: tuple[bool, list[set] | None]
    """
    partitions = []
    for ballot in instance.preferences:
        alt_set = set(ballot[0])
        new_set = True
        for s in partitions:
            if s == alt_set:
                new_set = False
                break
            elif len(alt_set.intersection(s)) > 0:
                return False, None
        if new_set:
            partitions.append(alt_set)
    return True, partitions


def is_2_part(instance):
    """
    Tests whether the given categorical instance is 2 partitions.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is 2 partitions and a
        partition of the candidates into two sets (or None if the instance is not 2 partitions).
    :rtype: tuple[bool, list[set] | None]
    """
    part_res = is_part(instance)
    if part_res[0] and len(part_res[1]) == 1:
        return part_res
    return False, None
