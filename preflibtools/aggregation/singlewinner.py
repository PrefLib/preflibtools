"""This module contains single-winner voting rules."""

from preflibtools.properties import requires_approval, requires_preference_type
from preflibtools.properties import borda_scores, copeland_scores

from collections import defaultdict


@requires_preference_type("soc", "toc", "soi", "toi")
def plurality_winner(instance):
    """Returns all the alternatives with the highest plurality score, i.e., that appear the highest number of times
    in first position.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = defaultdict(lambda: 0)
    for order, mult in instance.multiplicity.items():
        for a in order[0]:
            scores[a] += mult
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "toc")
def veto_winner(instance):
    """Returns all the alternatives with the smallest veto score, i.e., that appear the smallest number of times
    in the last indifference class.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = defaultdict(lambda: 0)
    for a in instance.alternatives_name:
        scores[a] = 0
    for order, mult in instance.multiplicity.items():
        for a in order[-1]:
            scores[a] += mult
    least_vetos = min(scores.values())
    return {a for a in scores if scores[a] == least_vetos}


@requires_preference_type("soc", "soi")
def k_approval_winner(instance, k):
    """Returns all the alternatives with the highest approval score, i.e., that appear the highest number of time in
    the first k positions. Only applies to strict rankings.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`

    :param k: The instance.
    :type k: int
    """
    scores = defaultdict(lambda: 0)
    for order, mult in instance.multiplicity.items():
        for x in order[:k]:
            a = x[0]
            scores[a] += mult
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "toc")
def borda_winner(instance):
    """Returns all the alternatives with the highest total Borda score.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = borda_scores(instance)
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc")
def copeland_winner(instance):
    """Returns the Copeland winners, i.e., the alternatives that win the highest number of pairwise comparisons.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    raw_scores = copeland_scores(instance)
    scores = dict()
    for a in raw_scores:
        scores[a] = sum(raw_scores[a].values())
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_approval
def approval_winner(instance):
    """Returns the approval winners, i.e., the alternatives with the highest approval score (number
    of appearance in the first position).

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    return plurality_winner(instance)


@requires_approval
def satisfaction_approval_winner(instance):
    """Returns the satisfaction approval winners, i.e., the alternatives with the highest
    satisfaction approval score (sum of 1 divided by length of the first position, for all
    approvers).

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = defaultdict(lambda: 0)
    for order, mult in instance.multiplicity.items():
        for a in order[0]:
            scores[a] += mult / len(order[0])
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "soi")
def fallback_voting_winner(instance):
    """Returns the fallback voting winners.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = defaultdict(lambda: 0)
    quota = (instance.num_voters // 2) + 1
    for order, mult in instance.multiplicity.items():
        scores[order[0][0]] = mult
    current_pos = 1
    current_max_value = -1
    while current_max_value < quota and current_pos < instance.num_alternatives:
        for order, mult in instance.multiplicity.items():
            if len(order) > current_pos:
                a = order[current_pos][0]
                scores[a] += mult
                current_max_value = max(current_max_value, scores[a])
        current_pos += 1
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc")
def bucklin_voting_winner(instance):
    """Returns the Bucklin winners.

    :param instance: The instance.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    scores = defaultdict(lambda: 0)
    quota = (instance.num_voters // 2) + 1
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        scores[order[0][0]] = multiplicity
    current_pos = 1
    current_max_value = -1
    while current_max_value < quota:
        for order in instance.orders:
            multiplicity = instance.multiplicity[order]
            if len(order) > current_pos:
                a = order[current_pos][0]
                scores[a] += multiplicity
                current_max_value = max(current_max_value, scores[a])
        current_pos += 1
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}
