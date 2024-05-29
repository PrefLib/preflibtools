from preflibtools.instances import CategoricalInstance
from interval import *
from partition import *

'''
Take dataset from PrefLib and check if subdomains exist in the data.
Append result (True or False) in a list to see all results of checked data sets
'''


data_list = ["https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000002.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000003.cat",
             "https://www.preflib.org/static/data/frenchapproval/00026-00000004.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000005.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000006.cat"]
data_list = ["https://www.preflib.org/static/data/kusama/00061-00000001.cat"]

CI_result = []
CEI_result = []
VI_result = []
VEI_result = []
part2_result = []
part_result = []

for approval_set in data_list:
    instance = CategoricalInstance()
    instance.parse_url(approval_set)
    instances = []
    for p in instance.preferences:
        preferences = p
        pref_set = set(preferences[0])
        if len(pref_set) > 0:
            instances.append(pref_set)
    
    res_CI, _ = is_CI(instances)
    res_CEI, _ = is_CEI(instances)
    res_VI, _ = is_VI(instances)
    res_VEI, _ = is_VEI(instances)

    res_2part, result_2part = is_2partition(instances)
    res_part, result_part = is_partition(instances)

    CI_result.append(res_CI)
    CEI_result.append(res_CEI)
    VI_result.append(res_VI)
    VEI_result.append(res_VEI)

    part2_result.append(res_2part)
    part_result.append(res_part)

print("CI:", CI_result)
print("CEI:", CEI_result)
print("VI:", VI_result)
print("VEI:", VEI_result)
print("2PART:", part2_result)
print("PART:", part_result)


# instance = CategoricalInstance()
# instance.parse_url("https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat")

# instances = []

# # Additional members of the class are related to the categories themselves
# instance.num_categories
# for cat, cat_name in instance.categories_name.items():
#     category = cat
#     name_of_the_category = cat_name
# # But also to the preferences
# for p in instance.preferences:
#     preferences = p
#     pref_set = set(preferences[0])
#     if len(pref_set) > 0:
#         instances.append(pref_set)
#     multiplicity = instance.multiplicity[p]
# instance.num_unique_preferences


# for a in instance.preferences[0][0]:
#     print(a)

# print(instances)
# print(len(instances))

# M, alternatives = instance_to_matrix(instances, interval='ci')
# print(M)

# instance_CEI = [
#     {'A'},
#     {'D', 'F', 'B'},
#     {'C', 'E'},
#     {'B', 'C', 'E'}
# ]

# instances = instance_CEI

# res_CI, result_CI = is_CI(instances)
# res_CEI, result_CEI = is_CEI(instances)
# res_VI, resul_VI = is_VI(instances)
# res_VEI, result_VEI = is_VEI(instances)

# print("CI:", res_CI)
# print("CEI:", res_CEI)
# print("VI:", res_VI)
# print("VEI:", res_VEI)

# res_2part, result_2part = is_2partition(instances)
# res_part, result_part = is_partition(instances)

# print("2part:", res_2part)
# print("PART:", res_part)
