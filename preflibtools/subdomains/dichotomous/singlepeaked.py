from interval import is_CI
from preflibtools.instances import CategoricalInstance

# Check Possibly Single-peaked
def is_PSP(instance_input):
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

    res, _ = is_CI(instance)

    if res is True:
        return True, None
    else:
        return False, None