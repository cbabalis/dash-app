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
    build_single_json_from_multiple_sheets(keys, dash_table, csv_table)
    # for each one get the unique values inside it
    #for (column_name, column_data) in csv_table.iteritems():
    #    dash_table[column_name] = list(column_data.unique())
    pdb.set_trace()
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
        

def get_table_unique_values(csv_table, column):
    """ Method to get the unique values from a table."""
    pass



def main():
    xlsx_tabs = read_xlsx(sys.argv[1])
    #z = xlsx_tabs.keys()
    #z = list(z)
    #a_tab = z[0]
    dt = get_table_unique_params(xlsx_tabs)
    pdb.set_trace()


if __name__ == '__main__':
    main()