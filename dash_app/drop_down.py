import dash
import dash_table
import dash_html_components as html
import pandas as pd

df = pd.read_csv('csv_files/Sheet1.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Συλλογή Ερευνητικών Εργασιών'),
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
        #fixed_rows={'headers': True, 'data': 0},
        #fixed_columns={'headers': True,'data': 1},#'headers': True,
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

if __name__ == '__main__':
    app.run_server(debug=True)