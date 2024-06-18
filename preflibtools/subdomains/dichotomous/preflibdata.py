from preflibtools.instances import CategoricalInstance
# from interval import *
# from partition import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
# from euclidean import *
# from singlecrossing import *


# '''
# Take dataset from PrefLib and check if subdomains exist in the data.
# Append result (True or False) in a list to see all results of checked data sets
# '''

# start_time = time.time()
# directory = '/Users/dennistol/Desktop/Studie/Scriptie/data/cat'
# data = []
# voters = []
# atlernatives = []
# file_number = 0
# count = 0
# for file in os.listdir(directory):
#     file_number += 1 
#     print(f"File number {file_number}")
#     filename = os.fsdecode(file)
#     instance = CategoricalInstance()
#     instance.parse_file(f'/Users/dennistol/Desktop/Studie/Scriptie/data/cat/{filename}')

#     file_name = instance.file_name
#     file_path = instance.file_path
#     title = instance.title
#     num_alt = instance.num_alternatives
#     num_voters = instance.num_voters
#     num_unique_pref = instance.num_unique_preferences
#     num_cat = instance.num_categories

#     instances = []

#     if num_cat <= 2:
#         categories = [cat_name for _, cat_name in instance.categories_name.items()]

#         for p in instance.preferences:
#             preferences = p
#             pref_set = set(preferences[0])
#             if len(pref_set) > 0:
#                 instances.append(pref_set)

#         print("CI")
#         res_CI, _ = is_CI(instances, show_result=False, show_matrix=False)

#         print("VI")
#         res_VI, _ = is_VI(instances, show_result=False, show_matrix=False)

#         if res_CI is False or res_VI is False:
#             res_2part = False
#             res_part = False
#             res_CEI = False
#             res_VEI = False
#             res_WSC = False
#             res_DUE = False
#             print("Done")
#         else:
#             print("DUE")
#             res_DUE = is_DUE(instances)

#             if res_DUE is False:
#                 res_2part = False
#                 res_part = False
#                 res_CEI = False
#                 res_VEI = False
#                 res_WSC = False
#                 print("Done")
#             else:
#                 print("WSC")
#                 if num_alt <= 350:
#                     res_WSC, _ = is_WSC(instances, show_result=False, show_matrix=False)
#                 else:
#                     res_WSC = None

#                 if res_WSC is False:
#                     res_2part = False

#                     print("part")
#                     res_part, result_part = is_PART(instances)


#                     print("CEI")
#                     res_CEI, _ = is_CEI(instances, show_result=False, show_matrix=False)


#                     print('VEI')
#                     res_VEI, _ = is_VEI(instances, show_result=False, show_matrix=False)
#                     print("Done")
#                 else:
#                     print("2part")
#                     res_2part, result_2part = is_2PART(instances)

#                     print("part")
#                     res_part, result_part = is_PART(instances)


#                     print("CEI")
#                     res_CEI, _ = is_CEI(instances, show_result=False, show_matrix=False)


#                     print('VEI')
#                     res_VEI, _ = is_VEI(instances, show_result=False, show_matrix=False)
#                     print("Done")


#         data.append([file_name, title, num_alt, num_voters, num_unique_pref, num_cat, categories, res_2part, res_part, res_CI, res_CEI, res_VI, res_VEI, res_WSC, res_DUE])


#         break


#     # if num_voters < 5000:

#     #     voters.append(num_voters)
#     #     atlernatives.append(num_alt)

# # plt.scatter(voters, atlernatives)
# # plt.xlabel('Voters count')
# # plt.ylabel('Alternatives count')
# # plt.title('Voter - alternative ratio files')
# # plt.show()
    


# df = pd.DataFrame(data, columns=['File name', 'Title', 'Num Alternatives', 'Num Voters', 'Num unique pref', 'Num categories', 'Categories', '2PART', 'PART', 'CI/DE/PE/PSP', 'CEI', 'VI', 'VEI', 'WSC', 'DUE'])

# print(df)
# df.to_excel("output_cat_data_all_results_TEST.xlsx") 
# df.to_csv('output_preflib_df_TEST')
# end_time = time.time()

# total_time = end_time - start_time
# print(f"Runtime: {total_time} seconds")

df = pd.read_csv('/Users/dennistol/Desktop/testfiles/output_preflib_df')

pd.set_option('display.max_rows', None)

# # print(df[df['PART'] == True])

# value_counts = df['PART'].value_counts()
# print(value_counts)

# value_counts = df['2PART'].value_counts()
# print(value_counts)

# value_counts = df['VI'].value_counts()
# print(value_counts)

# value_counts = df['CI/DE/PE/PSP'].value_counts()
# print(value_counts)

# value_counts = df['CEI'].value_counts()
# print(value_counts)

# value_counts = df['VEI'].value_counts()
# print(value_counts)

# value_counts = df['WSC'].value_counts()
# print(value_counts)

# value_counts = df['DUE'].value_counts()
# print(value_counts)


smaller_df = df[df['Num Voters'] >500]
end_df = smaller_df[smaller_df['Num Voters'] <1000000]
# df = df[df['VI'] == True]
# print(df)

print("Mean all voters:", round(df['Num unique pref'].mean(), 2))
# print("Mean all Alternatives:", round(df['Num unique pref'].mean(), 2))

print("Mean voters without big:", round(end_df['Num unique pref'].mean(),2))
# print("Mean alternatives without big:", round(end_df['Num unique pref'].mean(),2))

# plt.scatter(end_df['Num Voters'], end_df["Num Alternatives"])
# # plt.scatter(df["Num Alternatives"], df['Num Voters'])

# file_count = len(end_df)
# plt.xlabel('Voter count')
# plt.ylabel('Alternative count')
# plt.title(f'Distribution of Voters and Alternatives (Files: {file_count})')
# # plt.ylim(bottom=-5)
# # plt.xlim(left=-5)
# plt.show()


# df = df.drop(columns=['Title'])

# Convert to LaTeX table format
# latex_table = df.to_latex(index=False, longtable=True)

# Save the LaTeX table to a file
# with open('results_latex_new.tex', 'w') as f:
#     f.write(latex_table)
