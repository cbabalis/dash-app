""" Filters. https://dash.plotly.com/datatable/filtering"""

import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import xls_manipulation
import pdb


df = pd.read_csv('csv_files/teliko.csv') #diplomas_from_site.csv') # 1._Goods_Port_throughput.csv') #

#df['id'] = df['country']
#df.set_index('id', inplace=True, drop=False)

def get_dropdown_menu():
    dropdown_list = []
    already_met_list = []
    curr_table = {}
    for (column_name, column_data) in df.iteritems():
        curr_table[column_name] = list(column_data.unique())
    for key in curr_table:
        for val in curr_table[key]:
            if val not in already_met_list:
                dropdown_list.append(
                    {'label': val,
                    'value': val},
                )
                already_met_list.append(val)
            else:
                print(val)
    return dropdown_list

dl_list = get_dropdown_menu()

app = dash.Dash(__name__)


app.layout = html.Div([

    html.H1('1. Goods Port Throughput'),
    dcc.RadioItems(
        id='filter-query-read-write',
        options=[
            {'label': 'Read filter_query', 'value': 'read'},
            {'label': 'Write to filter_query', 'value': 'write'}
        ],
        value='read'
    ),

    html.Br(),
    
    html.Label('Dropdown menu'),
    dcc.Dropdown(
        id='Dropdown',
        options = dl_list, #[
        #    {'label': 'Cargo', 'value': 'Total'},
        #    {'label': 'Bulk', 'value': 'Dry Bulk'},
        #],
        multi=True,
    ),
    
    html.Br(),

    dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

    html.Div(id='filter-query-output'),

    html.Hr(),

    dash_table.DataTable(
        id='datatable-advanced-filtering',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        page_action='native',
        page_size=10,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_current= 0,
    ),
    
    html.Div(id='datatable-interactivity-container'),
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
])


@app.callback(
    [Output('filter-query-input', 'style'),
     Output('filter-query-output', 'style')],
    [Input('filter-query-read-write', 'value')]
)
def query_input_output(val):
    input_style = {'width': '100%'}
    output_style = {}
    if val == 'read':
        input_style.update(display='none')
        output_style.update(display='inline-block')
    else:
        input_style.update(display='inline-block')
        output_style.update(display='none')
    return input_style, output_style


@app.callback(
    Output('datatable-advanced-filtering', 'filter_query'),
    [Input('filter-query-input', 'value')]
)
def write_query(query):
    if query is None:
        return ''
    return query


@app.callback(
    Output('filter-query-output', 'children'),
    [Input('datatable-advanced-filtering', 'filter_query')]
)
def read_query(query):
    if query is None:
        return "No filter query"
    return dcc.Markdown('`filter_query = "{}"`'.format(query))


@app.callback(
    Output('datatable-query-structure', 'children'),
    [Input('datatable-advanced-filtering', 'derived_filter_query_structure')]
)
def display_query(query):
    if query is None:
        return ''
    return html.Details([
        html.Summary('Derived filter query structure'),
        html.Div(dcc.Markdown('''```json
{}
```'''.format(json.dumps(query, indent=4))))
    ])


@app.callback(
    Output('datatable-advanced-filtering', 'style_data_conditional'),
    [Input('datatable-advanced-filtering', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-advanced-filtering', "derived_virtual_data"),
     Input('datatable-advanced-filtering', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]
    
    
    all_vs_all = [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["Provider"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        #for column in ["Cargo", "Coverage"] if column in dff
        for column in df.columns if column in dff
    ]
    return all_vs_all



if __name__ == '__main__':
    app.run_server(debug=True)
