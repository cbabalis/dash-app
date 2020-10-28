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
    # get the column titles of the table
    columns = list(csv_table.columns.values)
    # for each one get the unique values inside it
    for (column_name, column_data) in csv_table.iteritems():
        dash_table[column_name] = list(column_data.unique())
    return dash_table

def get_table_unique_values(csv_table, column):
    """ Method to get the unique values from a table."""
    pass



def main():
    xlsx_tabs = read_xlsx(sys.argv[1])
    z = xlsx_tabs.keys()
    z = list(z)
    a_tab = z[0]
    dt = get_table_unique_params(xlsx_tabs[a_tab])
    pdb.set_trace()


if __name__ == '__main__':
    main()