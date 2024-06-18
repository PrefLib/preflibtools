from interval import instance_to_matrix, solve_C1


def is_WSC(instance, show_result=True, show_matrix=True):
    # Get matrix and lables
    M, columns_labels = instance_to_matrix(instance, interval='wsc')

    # Solve C1 and get results of new order columns
    res, ordered_idx = solve_C1(M)

    if res is False:
        return False, ([], [])
    else:
        # Get result of the order
        order_result = [columns_labels[i] for i in ordered_idx]

        # Convert result back to matrix based on column index
        M_result = M[:, ordered_idx]
    
    # Return depending on arguments
    if show_result is True:
        if show_matrix is True:
            return True, (order_result, M_result)
        else:
            return True, (order_result, [])
    else:
        if show_matrix is True:
            return True, ([], M_result)
        else:
            return True, ([], [])