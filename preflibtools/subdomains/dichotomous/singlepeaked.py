from interval import is_CI

# Check Possibly Single-peaked
def is_PSP(instance):
    res, _ = is_CI(instance)

    if res is True:
        return True, None
    else:
        return False, None