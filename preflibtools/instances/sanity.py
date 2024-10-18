import os.path
from operator import le, eq


def my_assert(condition, error, error_list):
    try:
        assert condition
    except AssertionError:
        print("ERROR: " + str(error))
        error_list.append(error)


def handle_my_assert(left, right, error_msg, error_list, op=eq):
    my_assert(
        op(left, right),
        error_msg.format(
            left, right
        ),
        error_list,
    )


def metadata(instance):
    """Checks that the basic metadata are in line with the content of the instance.

    :param instance: The instance to test.
    :type instance: :class:`preflibtools.instances.preflibinstance.PrefLibInstance`
    """

    error_list = []

    handle_my_assert(
        instance.data_type,
        os.path.splitext(instance.file_name)[1][1:],
        "Data type {} is not aligned with file extension {}",
        error_list
    )

    handle_my_assert(
        instance.num_alternatives,
        len(instance.alternatives_name),
        "Number of alternatives {} differs from number of alternative names {}",
        error_list
    )

    handle_my_assert(
        len(set(instance.alternatives_name.values())),
        instance.num_alternatives,
        "Some alternatives have the same name: {} != {}",
        error_list
    )
    return error_list


def orders(instance):
    """Checks that the orders are consistent.

    :param instance: The instance to draw.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """

    error_list = []

    handle_my_assert(
        len(instance.orders),
        len(instance.multiplicity),
        "len(orders) {} differs from len(order_multiplicity) {}",
        error_list
    )

    multiplicity_sum = sum(instance.multiplicity.values())
    handle_my_assert(
        instance.num_voters,
        multiplicity_sum,
        "Number of voters {} and number of orders seem different {}",
        error_list
    )

    handle_my_assert(
        instance.num_unique_orders,
        len(instance.orders),
        "Number of unique order {} differs from len(orders) {}",
        error_list
    )

    alternatives = set(
        alt for order in instance.orders for indif_class in order for alt in indif_class
    )

    handle_my_assert(
        len(alternatives),
        instance.num_alternatives,
        "More alternatives appear in the orders {} than in the header {}",
        error_list,
        le
    )

    my_assert(0 not in alternatives, "0 appears as an alternative", error_list)

    handle_my_assert(
        instance.data_type,
        instance.infer_type(),
        "Data type {} is not the same as the one inferred {}",
        error_list
    )

    handle_my_assert(
        len(set(instance.orders)),
        len(instance.orders),
        "Some orders appear several times: {} != {}",
        error_list
    )

    if len(set(instance.orders)) != len(instance.orders):
        for i in range(len(instance.orders)):
            order1 = instance.orders[i]
            for j in range(len(instance.orders)):
                if i != j:
                    order2 = instance.orders[j]
                    my_assert(
                        order1 != order2,
                        "Order {} at position {} is the same than order {} at position {}".format(
                            order1, i, order2, j
                        ),
                        error_list,
                    )

    for i in range(len(instance.orders)):
        order = instance.orders[i]
        alternatives_appearing = [alt for indif_class in order for alt in indif_class]
        num_alt_appearing = len(alternatives_appearing)
        num_unique_alt_appearing = len(set(alternatives_appearing))

        my_assert(
            num_alt_appearing <= instance.num_alternatives,
            "Order {} at position {} has too many alternatives".format(order, i),
            error_list,
        )

        my_assert(
            num_alt_appearing <= num_unique_alt_appearing,
            "Some alternatives appear several times in order {} at position {}".format(
                order, i
            ),
            error_list,
        )

        if instance.data_type in ["soc", "toc"]:
            my_assert(
                num_unique_alt_appearing <= instance.num_alternatives,
                "Order {} at position {} does not seem complete".format(order, i),
                error_list,
            )

        if instance.data_type in ["soc", "soi"]:
            my_assert(
                max(len(indif_class) for indif_class in order) == 1,
                "Order {} at position {} does not seem strict".format(order, i),
                error_list,
            )

    return error_list


def categories(instance):
    """Checks that the preferences and categories are consistent.

    :param instance: The instance to draw.
    :type instance: :class:`preflibtools.instances.preflibinstance.CategoricalInstance`
    """

    error_list = []

    handle_my_assert(
        len(instance.categories_name),
        instance.num_categories,
        "Number of category names {} differs from number of categories {}",
        error_list
    )

    handle_my_assert(
        len(instance.preferences),
        len(instance.multiplicity),
        "len(preferences) {} differs from len(multiplicity) {}",
        error_list,
    )

    multiplicity_sum = sum(instance.multiplicity.values())
    handle_my_assert(
        instance.num_voters,
        multiplicity_sum,
        "Number of voters {} and number of preferences seem different {}",
        error_list
    )

    handle_my_assert(
        instance.num_unique_preferences,
        len(instance.preferences),
        "Number of unique preferences {} differs from len(preferences) {}",
        error_list
    )

    alternatives = set(
        alt
        for order in instance.preferences
        for indif_class in order
        for alt in indif_class
    )
    handle_my_assert(
        len(alternatives),
        instance.num_alternatives,
        "More alternatives appear in the preference {} than in the header {}",
        error_list,
        le
    )

    my_assert(0 not in alternatives, "0 appears as an alternative", error_list)

    handle_my_assert(
        len(set(instance.preferences)),
        len(instance.preferences),
        "Some preferences appear several times: {} != {}",
        error_list
    )

    if len(set(instance.preferences)) != len(instance.preferences):
        for i in range(len(instance.preferences)):
            pref1 = instance.preferences[i]
            for j in range(len(instance.preferences)):
                if i != j:
                    pref2 = instance.preferences[j]
                    my_assert(
                        pref1 != pref2,
                        "Preference {} at position {} is the same than preference {} at position {}".format(
                            pref1, i, pref2, j
                        ),
                        error_list,
                    )

    for i in range(len(instance.preferences)):
        preference = instance.preferences[i]
        alternatives_appearing = [alt for category in preference for alt in category]
        num_alt_appearing = len(alternatives_appearing)
        num_unique_alt_appearing = len(set(alternatives_appearing))

        my_assert(
            num_alt_appearing <= instance.num_alternatives,
            "Preference {} at position {} has too many alternatives".format(
                preference, i
            ),
            error_list,
        )

        my_assert(
            num_alt_appearing <= num_unique_alt_appearing,
            "Some alternatives appear several times in preference {} at position {}".format(
                preference, i
            ),
            error_list,
        )

        my_assert(
            len(preference) == instance.num_categories,
            "Preference {} at position {} has {} categories instead of the {} expected.".format(
                preference, i, len(preference), instance.num_categories
            ),
            error_list,
        )

    return error_list


def matching(instance):
    """Checks that the matching preferences are consistent.

    :param instance: The instance to draw.
    :type instance: :class:`preflibtools.instances.preflibinstance.MatchingInstance`
    """
    pass
