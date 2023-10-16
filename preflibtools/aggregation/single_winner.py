"""This module contains single-winner voting rules."""

from preflibtools.aggregation.utilities import *
from preflibtools.properties.basic import *

@requires_preference_type("soc", "toc", "soi", "toi")
def plurality_winner(instance):
    scores = dict()
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        for a in order[0]:
            if a not in scores:
                scores[a] = multiplicity
            else:
                scores[a] += multiplicity
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "toc")
def veto_winner(instance):
    scores = {a : 0 for a in instance.alternatives_name}
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        for a in order[-1]:
            scores[a] += multiplicity
    least_vetos = min(scores.values())
    print(scores)
    return {a for a in scores if scores[a] == least_vetos}


@requires_preference_type("soc", "soi")
def k_approval_winner(instance, k):
    scores = dict()
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        tmp = k
        for x in order:
            a = x[0]
            if a not in scores:
                scores[a] = multiplicity
            else:
                scores[a] += multiplicity
            tmp -= 1
            if tmp <= 0:
                break
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "toc")
def borda_winner(instance):
    scores = borda_scores(instance)
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc")
def copeland_winner(instance):
    raw_scores = copeland_scores(instance)
    scores = dict()
    for a in raw_scores:
        scores[a] = sum(raw_scores[a].values())
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_approval
def approval_winner(instance):
    scores = dict()
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        for a in order[0]:
            if a not in scores:
                scores[a] = multiplicity
            else:
                scores[a] += multiplicity
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_approval
def satisfaction_approval_winner(instance):
    scores = dict()
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        for a in order[0]:
            if a not in scores:
                scores[a] = multiplicity/len(order[0])
            else:
                scores[a] += multiplicity/len(order[0])
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc", "soi")
def fallback_voting_winner(instance):
    scores = dict()
    quota = (instance.num_voters // 2) + 1
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        scores[order[0][0]] = multiplicity
    current_pos = 1
    while max(scores.values()) < quota and current_pos < instance.num_alternatives:
        for order in instance.orders:
            multiplicity = instance.multiplicity[order]
            if len(order) > current_pos:
                a = order[current_pos][0]
                if a not in scores:
                    scores[a] = multiplicity
                else:
                    scores[a] += multiplicity
        current_pos += 1
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}


@requires_preference_type("soc")
def bucklin_voting_winner(instance):
    scores = dict()
    quota = (instance.num_voters // 2) + 1
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        scores[order[0][0]] = multiplicity
    current_pos = 1
    while max(scores.values()) < quota:
        for order in instance.orders:
            multiplicity = instance.multiplicity[order]
            if len(order) > current_pos:
                a = order[current_pos][0]
                if a not in scores:
                    scores[a] = multiplicity
                else:
                    scores[a] += multiplicity
        current_pos += 1
    best_score = max(scores.values())
    return {a for a in scores if scores[a] == best_score}