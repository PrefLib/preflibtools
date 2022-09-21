# # THIS IS JUST TO MAKE SURE THERE ARE NO TYPO IN THE USAGE EXAMPLES, DO NOT PUSH UNCOMMENTED VERSION TO THE GIT


# from preflibtools.instances import PrefLibInstance
#
# # The instance can be populated either by reading a file, or from an URL.
# instance = PrefLibInstance()
# instance.parse_file("00001-00000001.soi")
# instance.parse_url("https://www.preflib.org/static/data/irish/00001-00000001.soi")
#
# instance.file_path
# instance.file_name
# # The type of the instance and its modification type
# instance.data_type
# instance.modification_type
# # Some potentially related files
# instance.relates_to
# instance.related_files
# # The title of the data file and its description (mainly empty, on purpose)
# instance.title
# instance.description
# # Some historical landmark about the data file
# instance.publication_date
# instance.modification_date
# # The number of alternatives and their names
# instance.num_alternatives
# for alt, alt_name in instance.alternatives_name.items():
#     alternative = alt
#     name = alt_name
# # The number of voters
# instance.num_voters
#
# instance.write(path_to_the_file)
#
# from preflibtools.instances import OrdinalInstance
#
# # We can populate the instance by reading a file from PrefLib.
# # You can do it based on a URL or on a path to a file
# instance = OrdinalInstance()
# instance.parse_file("00001-00000001.soi")
# instance.parse_url("https://www.preflib.org/static/data/irish/00001-00000001.soi")
#
# # Additional members of the class are the orders,  their multiplicity and the number of unique orders
# for o in instance.orders:
#     order = o
#     multiplicity = instance.multiplicity[order]
# instance.num_unique_orders
#
# strict_order = ((1,), (2,), (0,))
# # The weak and complete order (1, 2) > 0 > (3, 4)
# weak_order = ((1, 2), (0,), (3, 4))
# # The incomplete an weak order (1, 2) > 4
# incomplete_order = ((1, 2), (4,))
#
# # Adding preferences to the instance, using different formats
# # Simply a list of orders
# extra_orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
# instance.append_order_list(extra_orders)
# # A vote map, i.e., a dictionary mapping orders to their multiplicity
# extra_vote_map = {((0,), (1,), (2,)): 3, ((2,), (0,), (1,)): 2}
# instance.append_vote_map(extra_vote_map)
#
# # We can access the full profile, i.e., with orders appearing several times
# # (according to their multiplicity)
# instance.full_profile()
#
# # If we are dealing with strict orders, we can flatten the orders so that ((0,), (1,), (2,))
# # is rewritten as (0, 1, 2). This return a list of tuple(order, multiplicity).
# instance.flatten_strict()
#
# # We can access the profile as a vote map
# instance.vote_map()
#
# # Some statistical culture we provide, here for 5 voters and 10 alternatives
# instance = OrdinalInstance()
# instance.populate_mallows_mix(5, 10, 3)
# instance.populate_urn(5, 10, 76)
# instance.populate_IC(5, 10)
# instance.populate_IC_anon(5, 10)
#
# from preflibtools.properties import borda_scores, has_condorcet
#
# # Let's check the Borda scores of the alternatives
# borda_scores(instance)
# # We can also check if the instance has a Condorcet winner
# has_condorcet(instance)
#
# from preflibtools.properties.singlepeakedness import *
#
# # We can first check if the instance is single-peaked with respect to a given
# # axis. This only works for complete orders, they can be weak though.
# is_SP = is_single_peaked_axis(instance, [0, 1, 2])
# # In general we can test for the single-peakedness of the instance:
# # In the case of strict and complete orders;
# (is_SP, axis) = is_single_peaked(instance)
# # And in the case of weak and complete order (using an ILP solver).
# (is_SP, opt_status, axis) = is_single_peaked_ILP(instance)
#
# # Maybe the instance is not single-peaked, but approximately. We can check how close to
# # single-peaked it is in terms of voter deletion and alternative deletion.
# (num_voter_deleted, opt_status, axis, deleted_voters) = approx_SP_voter_deletion_ILP(instance)
# (num_alt_deleted, opt_status, axis, deleted_alts) = approx_SP_alternative_deletion_ILP(instance)
#
# from preflibtools.properties.singlecrossing import is_single_crossing
#
# # Testing if the instance is single-crossing
# is_single_crossing(instance)
#
# from preflibtools.properties.distances import distance_matrix, spearman_footrule_distance
# from preflibtools.properties.distances import kendall_tau_distance, sertel_distance
#
# # We can create the distance matrix between any two orders of the instance
# distance_matrix(instance, kendall_tau_distance)
# distance_matrix(instance, spearman_footrule_distance)
# distance_matrix(instance, sertel_distance)
#
# from preflibtools.instances import CategoricalInstance
#
# instance = CategoricalInstance()
# instance.parse_url("https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat")
#
# # Additional members of the class are related to the categories themselves
# instance.num_categories
# for cat, cat_name in instance.categories_name.items():
#     category = cat
#     name_of_the_category = cat_name
# # But also to the preferences
# for p in instance.preferences:
#     preferences = p
#     multiplicity = instance.multiplicity[p]
# instance.num_unique_preferences
#
# from preflibtools.instances import CategoricalInstance
#
# instance = CategoricalInstance()
# instance.parse_url("https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat")
#
# # Additional members of the class are related to the categories themselves
# instance.num_categories
# for cat, cat_name in instance.categories_name.items():
#     category = cat
#     name_of_the_category = cat_name
# # But also to the preferences
# for p in instance.preferences:
#     preferences = p
#     multiplicity = instance.multiplicity[p]
# instance.num_unique_preferences