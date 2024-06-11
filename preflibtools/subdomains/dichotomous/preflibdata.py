from preflibtools.instances import CategoricalInstance
from interval import *
from partition import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import time


'''
Take dataset from PrefLib and check if subdomains exist in the data.
Append result (True or False) in a list to see all results of checked data sets
'''


# data_list = ["https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000002.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000003.cat",
#              "https://www.preflib.org/static/data/frenchapproval/00026-00000004.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000005.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000006.cat"]
# data_list = ["https://www.preflib.org/static/data/kusama/00061-00000001.cat", "https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat"]
start_time = time.time()
directory = '/Users/dennistol/Desktop/Studie/Scriptie/data/cat'
data = []
voters = []
atlernatives = []
file_number = 0
for file in os.listdir(directory):
    file_number += 1 
    print(f"File number {file_number}")
    filename = os.fsdecode(file)
    instance = CategoricalInstance()
    instance.parse_file(f'/Users/dennistol/Desktop/Studie/Scriptie/data/cat/{filename}')

    file_name = instance.file_name
    file_path = instance.file_path
    title = instance.title
    num_alt = instance.num_alternatives
    num_voters = instance.num_voters
    num_unique_pref = instance.num_unique_preferences
    num_cat = instance.num_categories

    instances = []

    if num_cat <= 2:
        categories = [cat_name for _, cat_name in instance.categories_name.items()]

        for p in instance.preferences:
            preferences = p
            pref_set = set(preferences[0])
            if len(pref_set) > 0:
                instances.append(pref_set)

        # print("2part")
        # res_2part, result_2part = is_2PART(instances)

        # print("part")
        # res_part, result_part = is_PART(instances)

        # print("CI")
        # res_CI, _ = is_CI(instances, show_result=False, show_matrix=False)

        # print("CEI")
        # res_CEI, _ = is_CEI(instances, show_result=False, show_matrix=False)

        # print("VI")
        # res_VI, _ = is_VI(instances, show_result=False, show_matrix=False)

        # print('VEI')
        # res_VEI, _ = is_VEI(instances, show_result=False, show_matrix=False)
        if num_alt <= 500:
            print(file_name)
            print(num_alt)
            print(num_voters)
            print(num_unique_pref)

            print("WSC")
            res_WSC, _ = is_WSC(instances, show_result=False, show_matrix=False)

            print("Done")
            data.append([file_name, title, num_alt, num_voters, num_unique_pref, num_cat, categories, res_WSC])
                        #  res_2part, res_part, res_CI, res_CEI, res_VI, res_VEI, res_WSC])
        else:
            continue
        
        # break
    print(data)

    # if num_voters < 5000:

    #     voters.append(num_voters)
    #     atlernatives.append(num_alt)

# plt.scatter(voters, atlernatives)
# plt.xlabel('Voters count')
# plt.ylabel('Alternatives count')
# plt.title('Voter - alternative ratio files')
# plt.show()
    


df = pd.DataFrame(data, columns=['File name', 'Title', 'Num Alternatives', 'Num Voters', 'Num unique pref', 'Num categories', 'Categories', 'WSC'])
                                #  '2PART', 'PART', 'CI', 'CEI', 'VI', 'VEI', 'WSC'])

print(df)
# df.to_excel("output_cat_data_tested.xlsx") 
end_time = time.time()

total_time = start_time - end_time
print(f"Runtime: {total_time} seconds")

    

# CI_result = []
# CEI_result = []
# VI_result = []
# VEI_result = []
# part2_result = []
# part_result = []

# for approval_set in data_list:
#     instance = CategoricalInstance()
#     instance.parse_url(approval_set)
#     instances = []
#     for p in instance.preferences:
#         preferences = p
#         pref_set = set(preferences[0])
#         if len(pref_set) > 0:
#             instances.append(pref_set)
    
#     res_CI, _ = is_CI(instances)
#     res_CEI, _ = is_CEI(instances)
#     res_VI, _ = is_VI(instances)
#     res_VEI, _ = is_VEI(instances)

#     res_2part, result_2part = is_2PART(instances)
#     res_part, result_part = is_PART(instances)

#     CI_result.append(res_CI)
#     CEI_result.append(res_CEI)
#     VI_result.append(res_VI)
#     VEI_result.append(res_VEI)

#     part2_result.append(res_2part)
#     part_result.append(res_part)

# print("CI:", CI_result)
# print("CEI:", CEI_result)
# print("VI:", VI_result)
# print("VEI:", VEI_result)
# print("2PART:", part2_result)
# print("PART:", part_result)


# instance = CategoricalInstance()
# instance.parse_url("https://www.preflib.org/static/data/frenchapproval/00026-00000001.cat")
# instance.parse_url("https://www.preflib.org/static/data/kusama/00061-00000001.cat")

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
# num = instance.num_unique_preferences
# num_cat = instance.num_categories

# print(num_cat)
# print(instances)

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
