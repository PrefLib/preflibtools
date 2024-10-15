from preflibtools.properties.subdomains.dichotomous.euclidean import is_dichotomous_euclidean
from preflibtools.properties.subdomains.dichotomous.interval import is_candidate_interval, is_candidate_extremal_interval, is_voter_interval, is_voter_extremal_interval
from preflibtools.properties.subdomains.dichotomous.partition import is_part, is_2_part
from preflibtools.properties.subdomains.dichotomous.singlecrossing import is_weakly_single_crossing

__all__ = [
    "is_part",
    "is_2_part",
    "is_voter_interval",
    "is_voter_extremal_interval",
    "is_candidate_interval",
    "is_candidate_extremal_interval",
    "is_weakly_single_crossing",
    "is_dichotomous_euclidean"
]
