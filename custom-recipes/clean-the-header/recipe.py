# -*- coding: utf-8 -*-

import dataiku
import pandas as pd, numpy as np
import re
import unicodedata
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

#Inputs Management:
L_input_datasets = get_input_names_for_role('input_dataset')
INPUT_DATASET = dataiku.Dataset(L_input_datasets[0]) 

#Outputs Management:
L_output_datasets = get_output_names_for_role('output_dataset')
OUTPUT_DATASET = dataiku.Dataset(L_output_datasets[0])

#Parameters Management:
uppercase_or_lowercase = get_recipe_config()['uppercase_or_lowercase']

#Read recipe inputs :
df_input = INPUT_DATASET.get_dataframe()
L_cols = list(df_input.columns)

def remove_accents(x):

    return unicodedata.normalize('NFD',x).encode('ascii', 'ignore')

def clean_string_col(string_value):

    string_value = re.sub("[\.\-,' ]", '_', string_value)

    string_value = remove_accents(string_value)
    if uppercase_or_lowercase == "lowerercase":
        string_value = str.lower(string_value)
        
    elif uppercase_or_lowercase == "uppercase":
        string_value = str.upper(string_value)
    else:
        string_value = str.lower(string_value)
        
    return string_value

L_clean_cols = [clean_string_col(col) for col in L_cols]

for col, clean_col in zip(L_cols, L_clean_cols):
    df_input.rename({col:clean_col}, axis=1, inplace=True)

df_output = df_input # For this sample code, simply copy input to output

#Write recipe outputs :
OUTPUT_DATASET.write_with_schema(df_output)