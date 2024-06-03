from interval import is_CI


# Check Dichotomous Euclidean
def is_DE(instance):
    res, _ = is_CI(instance)

    if res is True:
        return True, None
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
    pass