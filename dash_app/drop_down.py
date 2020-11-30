import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import pdb



df = pd.read_csv('csv_files/Sheet1.csv')

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

def show_callbacks(app):
    
    def format_regs(registrations, padding=10):
        # TODO: -- switch to single line printing if > 79 chars                                                                                                                                
        vals = sorted("{}.{}".format(i['id'], i['property'])
                      for i in registrations)
        return ", ".join(vals)

    output_list = []

    for callback_id, callback in app.callback_map.items():
        wrapped_func = callback['callback'].__wrapped__
        inputs = callback['inputs']
        states = callback['state']
        events = callback['events']

        str_values = {
            'callback': wrapped_func.__name__,
            'output': callback_id,
            'filename': os.path.split(wrapped_func.__code__.co_filename)[-1],
            'lineno': wrapped_func.__code__.co_firstlineno,
            'num_inputs': len(inputs),
            'num_states': len(states),
            'num_events': len(events),
            'inputs': format_regs(inputs),
            'states': format_regs(states),
            'events': format_regs(events)
        }

        output = """                                                                                                                                                                           
        callback      {callback} @ {filename}:{lineno}                                                                                                                                         
        Output        {output}                                                                                                                                                                 
        Inputs  {num_inputs:>4}  {inputs}                                                                                                                                                      
        States  {num_states:>4}  {states}                                                                                                                                                      
        Events  {num_events:>4}  {events}                                                                                                                                                      
        """.format(**str_values)

        output_list.append(output)
    return "\n".join(output_list)

if __name__ == '__main__':
    app.run_server(debug=True)