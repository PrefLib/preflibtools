from interval import instance_to_matrix, solve_consecutive_ones
from preflibtools.instances import CategoricalInstance


def is_WSC(instance_input):
    if isinstance(instance_input, CategoricalInstance):
        # Convert categorical instance to usable format
        instance = []
        for p in instance_input.preferences:
            preferences = p
            pref_set = set(preferences[0])
            if len(pref_set) > 0:
                instance.append(pref_set)
    else:
        instance = instance_input

    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='wsc')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_consecutive_ones(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]
    
    return True, (order_result, M_result)