from preflibtools.instances import CategoricalInstance
from interval import *
from partition import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from euclidean import *
from singlecrossing import *


'''
Take dataset from PrefLib and check if subdomains exist in the data.
Append result (True or False) in a list to see all results of checked data sets
'''

start_time = time.time()
directory = 'ENTER YOUR DIRECTORY'
data = []
voters = []
atlernatives = []
file_number = 0
count = 0
for file in os.listdir(directory):
    file_number += 1 
    print(f"File number {file_number}")
    filename = os.fsdecode(file)
    instance = CategoricalInstance()
    file_path = os.path.join(directory + filename)
    instance.parse_file(file_path)

    file_name = instance.file_name
    file_path = instance.file_path
    title = instance.title
    num_alt = instance.num_alternatives
    num_voters = instance.num_voters
    num_unique_pref = instance.num_unique_preferences
    num_cat = instance.num_categories


    if num_cat <= 2:
        categories = [cat_name for _, cat_name in instance.categories_name.items()]


        print("CI")
        res_CI, _ = is_CI(instance)

        print("VI")
        res_VI, _ = is_VI(instance)

        if res_CI is False or res_VI is False:
            res_2part = False
            res_part = False
            res_CEI = False
            res_VEI = False
            res_WSC = False
            res_DUE = False
            print("Done")
        else:
            print("DUE")
            res_DUE = is_DUE(instance)

            if res_DUE is False:
                res_2part = False
                res_part = False
                res_CEI = False
                res_VEI = False
                res_WSC = False
                print("Done")
            else:
                print("WSC")
                if num_alt <= 350:
                    res_WSC, _ = is_WSC(instance)
                else:
                    res_WSC = None

                if res_WSC is False:
                    res_2part = False

                    print("part")
                    res_part, result_part = is_PART(instance)


                    print("CEI")
                    res_CEI, _ = is_CEI(instance)


                    print('VEI')
                    res_VEI, _ = is_VEI(instance)
                    print("Done")
                else:
                    print("2part")
                    res_2part, result_2part = is_2PART(instance)

                    print("part")
                    res_part, result_part = is_PART(instance)


                    print("CEI")
                    res_CEI, _ = is_CEI(instance)


                    print('VEI')
                    res_VEI, _ = is_VEI(instance)
                    print("Done")


        data.append([file_name, title, num_alt, num_voters, num_unique_pref, num_cat, categories, res_2part, res_part, res_CI, res_CEI, res_VI, res_VEI, res_WSC, res_DUE])



df = pd.DataFrame(data, columns=['File name', 'Title', 'Num Alternatives', 'Num Voters', 'Num unique pref', 'Num categories', 'Categories', '2PART', 'PART', 'CI/DE/PE/PSP', 'CEI', 'VI', 'VEI', 'WSC', 'DUE'])

df.to_excel("output_cat_data_all_results.xlsx") 
df.to_csv('output_preflib_df')
end_time = time.time()

total_time = end_time - start_time
print(f"Runtime: {total_time} seconds")