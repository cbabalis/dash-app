import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate
import pdb


def get_list_options(df):
    """ Method to get all unique values of the dataframe."""
    # get columns' names (like keys)
    columns = [c for c in df.columns]
    # based on columns' names create a dictionary of
    # <column name: unique_values_list> pairs.
    all_col_value_list = []
    for c in columns:
        all_col_value_list = get_option(df, c)
    #     all_col_value_list.append([{'label':c_val, 'value':c_val}
    #                                for c_val in df[c].unique()])
    return all_col_value_list


def get_option(df, col_name):
    options_list = []
    options_list.append([{'label':c_val, 'value':c_val}
                            for c_val in df[col_name].unique()])
    return options_list



df = pd.read_csv('csv_files/Sheet1.csv')


def get_str_dtype(df, col):
    """Return dtype of col in df"""
    dtypes = [c for c in df.columns]
    for d in dtypes:
        try:
            if d in str(df.dtypes.loc[col]).lower():
                return d
        except KeyError:
            return None

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Συλλογή Ερευνητικών Εργασιών'),
    html.Div(id='container_col_select',
                 children=dcc.Dropdown(id='col_select',
                                       options=[{
                                           'label': c.replace('_', ' ').title(),
                                           'value': c}
                                           for c in df.columns]),
                 style={'display': 'inline-block', 'width': '16%', 'margin-left': '7%'}),
    html.Div(id='dropdown_selection',
                children=dcc.Dropdown(id='cat_filter', multi=True,
                                       options=get_list_options(df))),
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
        },
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        css=[{
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                line-height: 15px;
                max-height: 30px; min-height: 30px; height: 30px;
                display: block;
                overflow-y: hidden;
            '''
        }],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('rows')
        ],
        tooltip_duration=None,
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '110px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal',
            'textAlign': 'left'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Έτος'},
            'width': '20px'},
            {'if': {'column_id': 'Λινκ στο openarchives'},
            'width': '40px'},
            {'if': {'column_id': 'ΣΕΛΙΔΑ ΣΤΟ OPEN ARCHIVES'},
            'width': '40px'},
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 228)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        data=df.to_dict('records'),
        editable=True,
        page_action='native',
        page_size=20,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        style_table={'overflowX': 'auto'},
        selected_columns=[],
        selected_rows=[],
        page_current= 0,
    )
])

@app.callback([Output(x, 'style')
               for x in ['dropdown_selection']],
              [Input('col_select', 'value')])
def display_relevant_filter_container(col):
    if col is None:
        return [{'display': 'none'} for i in range(5)]
    dtypes = [c for c in df.columns]
    result = [{'display': 'none'} if get_str_dtype(df, col) not in d
              else {'display': 'inline-block',
                    'margin-left': '7%',
                    'width': '400px'} for d in dtypes]
    return result


@app.callback(Output('table', 'data'),
              [Input('col_select', 'value'),
               Input('cat_filter', 'value'),
               #Input('bool_filter', 'value'),
            ])
def filter_table(col, categories):
                 #bool_filter, start_date, end_date):
    if all([param is None for param in [col, categories]]):
        raise PreventUpdate
    if  categories and (get_str_dtype(df, col)): # == 'category'):
        df = df[df[col].isin(categories)]
        return df.to_dict('rows')
    else:
        return df.to_dict('rows')


if __name__ == '__main__':
    app.run_server(debug=True)