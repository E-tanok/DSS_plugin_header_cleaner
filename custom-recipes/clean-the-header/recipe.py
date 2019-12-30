# Code for custom code recipe clean-the-header (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -*- coding: utf-8 -*-

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re
import unicodedata

INPUT_DATASET = "CartoStructure_4T18"

OUTPUT_DATASET = "CartoStructure_4T18_clean_header"

# Read recipe inputs

dataset_input = dataiku.Dataset(INPUT_DATASET)

df_input = dataset_input.get_dataframe()
L_cols = list(df_input.columns)

def remove_accents(x):

    return unicodedata.normalize('NFD',x).encode('ascii', 'ignore')

def clean_string_col(string_value):

    string_value = re.sub("[\.\-,' ]", '_', string_value)

    string_value = remove_accents(string_value)

    string_value = str.lower(string_value)

    return string_value

L_clean_cols = [clean_string_col(col) for col in L_cols]

for col, clean_col in zip(L_cols, L_clean_cols):
    df_input.rename({col:clean_col}, axis=1, inplace=True)


df_output = df_input # For this sample code, simply copy input to output

# Write recipe outputs

header_clean_dataset = dataiku.Dataset(OUTPUT_DATASET)

header_clean_dataset.write_with_schema(df_output)