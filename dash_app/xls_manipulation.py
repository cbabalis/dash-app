# -*- coding: utf-8 -*-

# Run this app with 'python dash-app.py' and visit
# http://127.0.0.1:8050 in your web browser.

# This module reads an xlsx file (user has it as input), converts data to
# appropriate form and it uses dash in order to show them online.

# author: Babis Babalis babisbabalis@gmail.com

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sys

import pdb


def read_xlsx(filename):
    """ Method to read an xlsx file.
    """
    xl_file = pd.ExcelFile(filename)
    dfs = {sheet_name: xl_file.parse(sheet_name)
            for sheet_name in xl_file.sheet_names}
    return dfs


def get_table_unique_params(csv_table):
    """ Method to get the unique parameters (columns) of a table.
    TODO write doc here.
    """
    dash_table = {}
    # modify the table in order to further proccess its data
    keys = csv_table.keys()
    keys = list(keys)
    # build a single large json file with all sheets and their contents inside.
    build_single_json_from_multiple_sheets(keys, dash_table, csv_table)
    return dash_table


def build_single_json_from_multiple_sheets(keys, dash_table, csv_table):
    """ Method which takes as input a big csv_table containing sheets of
    excel and panda objects and by iterating the keys, it constructs a
    big json file from with column titles being keys in the new dictionary.
    """
    # for each sheet title
    for key in keys:
        # acquire the sheet (in pandas form)
        current_sheet = csv_table[key]
        # and iterate in acquiring all the unique values of it
        curr_table = {}
        for (column_name, column_data) in current_sheet.iteritems():
            # add the contents of it to a dictionary
            curr_table[column_name] = list(column_data.unique())
        # finally add this dictionary as value of a new dictionary with key
        # being the initial key (sheet name)
        dash_table[key] = curr_table


def convert_excel_to_csvs(xls_file_path, csv_folder_path):
    """ Method to convert an xls file to csv file(s).
    Each sheet of xls is converted to a single csv file.
    """
    dfs = read_xlsx(xls_file_path)
    for df in dfs:
        filename = "{}/{}.csv".format(csv_folder_path, df)
        dfs[df].to_csv(filename, index=None, header=True)


def get_dash_dropdown_list_from_dataframe(unique_values_dict):
    """ Method to get a dictionary ready to be used to a dropdown menu
    to dash dropdown.

    Args:
        unique_values_dict (dict): A dictionary of unique values for columns.
    """
    dropdown_list = []
    # return an object of the form:
    # {label: 'key', 'value':[list of values]}
    for k in unique_values_dict:
        dropdown_list.append({'label': k, 'value': unique_values_dict[k]})
    return dropdown_list


def main():
    xlsx_tabs = read_xlsx(sys.argv[1])
    dt = get_table_unique_params(xlsx_tabs)
    pdb.set_trace()
    convert_excel_to_csvs(sys.argv[1], 'csv_files')


if __name__ == '__main__':
    main()