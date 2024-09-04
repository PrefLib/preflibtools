from preflibtools.instances import CategoricalInstance


def initialise_categorical_instance(num_alternatives):
    instance = CategoricalInstance()
    instance.categories_name = ["Approved"]
    instance.num_categories = len(instance.categories_name)
    instance.num_alternatives = num_alternatives
    instance.alternatives_name = {j: j for j in range(num_alternatives)}
    return instance
