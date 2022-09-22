""" This module describes procedures to sample preferences for different probability distributions.
"""

import numpy as np

def generate_mallows(num_voters, num_alternatives, mixture, dispersions, references):
    """ Generates a profile following a mixture of Mallow's models.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param num_alternatives: Number of alternatives for the sampled orders.
        :type num_alternatives: int
        :param mixture: A list of the weights of each element of the mixture.
        :type mixture: list of positive numbers
        :param dispersions: A list of the dispersion coefficient of each element of the mixture.
        :type dispersions: list of float
        :param references: A list of the reference orders for each element of the mixture.
        :type references: list of tuples of tuples of int

        :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
            the given order as their preferences.
        :rtype: dict
    """

    def mallows_insert_distributions(num_alternatives, phi):
        distributions = {}
        for i in range(1, num_alternatives + 1):
            # Start with an empty distro of length i
            distribution = [0] * i
            # compute the denom = phi^0 + phi^1 + ... phi^(i-1)
            denominator = sum([pow(phi, k) for k in range(i)])
            # Fill each element of the distro with phi^(i-j) / denominator
            for j in range(1, i + 1):
                distribution[j - 1] = pow(phi, i - j) / denominator
            distributions[i] = distribution
        return distributions

    if len(mixture) != len(dispersions) or len(mixture) != len(references):
        raise ValueError("Parameters of Mallows' mixture do not have the same length.")
    # We normalize the mixture so that it sums up to 1
    if sum(mixture) != 1:
        mixture = [m / sum(mixture) for m in mixture]

    # Precompute the distros for each Phi.
    insert_distributions = []
    for i in range(len(mixture)):
        insert_distributions.append(mallows_insert_distributions(num_alternatives, dispersions[i]))

    # Now, generate votes...
    vote_map = {}
    for voter in range(num_voters):
        model = np.random.choice(range(len(mixture)), 1, p=mixture)[0]

        # Generate a vote for the selected model
        insert_vector = [0] * num_alternatives
        for i in range(1, len(insert_vector) + 1):
            # options are 1...max
            insert_vector[i - 1] = np.random.choice(range(1, i + 1), 1, p=insert_distributions[model][i])[0]

        vote = []
        for i in range(len(references[model])):
            vote.insert(insert_vector[i] - 1, references[model][i])

        vote = tuple((alt,) for alt in vote)
        vote_map[vote] = vote_map.get(vote, 0) + 1

    return vote_map


def generate_mallows_mix(num_voters, alternatives, num_references):
    """ Generates a profile following a mixture of Mallow's models for which reference points and dispersion 
        coefficients are independently and identically distributed.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param alternatives: List of alternatives for the sampled orders.
        :type alternatives: list of int
        :param num_references: Number of element
        :type num_references: int

        :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
            the given order as their preferences.
        :rtype: dict
    """
    mixture = []
    dispersions = []
    references = []
    for i in range(num_references):
        references.append(tuple(generate_IC(1, alternatives))[0])
        dispersions.append(round(np.random.rand(), 5))
        mixture.append(np.random.randint(1, 101))
    mixture = [float(i) / float(sum(mixture)) for i in mixture]
    return generate_mallows(num_voters, len(alternatives), mixture, dispersions, references)


def generate_urn(num_voters, alternatives, replace):
    """ Generates a profile following the urn model.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param alternatives: List of alternatives.
        :type alternatives: list of int
        :param replace: The number of replacements for the urn model.
        :type replace: int

        :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
            the given order as their preferences.
        :rtype: dict
    """
    vote_map = {}
    replace_votes = {}

    if len(alternatives) > 20:
        raise ValueError("Because of normalisation factors involving a factorial, we cannot run an urn sampling with "
                         "mor than 20 alternatives.")

    IC_size = np.math.factorial(len(alternatives))
    replace_size = 0

    for x in range(num_voters):
        flip = np.random.randint(1, IC_size + replace_size + 1)
        # We either draw an "original vote"
        if flip <= IC_size:
            # generate an IC vote and make a suitable number of replacements...
            vote = generate_IC_ballot(alternatives)
            vote_map[vote] = (vote_map.get(vote, 0) + 1)
            replace_votes[vote] = (replace_votes.get(vote, 0) + replace)
            replace_size += replace
        else:
            # iterate over replacement hash and select proper vote.
            flip = flip - IC_size
            for vote in replace_votes.keys():
                flip = flip - replace_votes[vote]
                if flip <= 0:
                    vote_map[vote] = (vote_map.get(vote, 0) + 1)
                    replace_votes[vote] = (replace_votes.get(vote, 0) + replace)
                    replace_size += replace
                    break

    return vote_map


def generate_IC(num_voters, alternatives):
    """ Generates a profile of strict preferences following the impartial culture.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param alternatives: List of alternatives.
        :type alternatives: list of int

        :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
            the given order as their preferences.
        :rtype: dict
    """
    return generate_urn(num_voters, alternatives, 0)


def generate_IC_anon(num_voters, alternatives):
    """ Generates a profile of strict preferences following the anonymous impartial culture.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param alternatives: List of alternatives.
        :type alternatives: list of int

        :return: A vote map, i.e., a dictionary whose keys are orders, mapping to the number of voters with
            the given order as their preferences.
        :rtype: dict
    """
    return generate_urn(num_voters, alternatives, 1)


def generate_IC_ballot(alternatives):
    """ Generates a strict order over the set of alternatives following the impartial culture.

        :param alternatives: List of alternatives.
        :type alternatives: list of int

        :return: A strict order over the alternatives, i.e., a tuple of tuples of size 1.
        :rtype: tuple
    """
    options = list(alternatives)
    vote = []
    while len(options) > 0:
        # randomly select an option
        vote.append(options.pop(np.random.randint(0, len(options))))
    return tuple((alt,) for alt in vote)
