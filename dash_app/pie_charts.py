import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import pdb


df = pd.read_csv('csv_files/Sheet1.csv')
dfs = px.data.tips()
# get years column. Then acquire the unique values
years = [x for x in df][2]
years_val = df[years].unique()


def display_datespan_graph(df):
    x = df.columns[2]
    min_df, max_df = int(min(df[x])), int(max(df[x]))
    counts, bins = np.histogram(df[x], bins=range(min_df, max_df, 4))
    bins = 0.5 * (bins[:-1] + bins[1:])
    datespan_fig = px.bar(x=bins, y=counts, labels={'x':'time span', 'y':'count'})
    return datespan_fig


def display_datespan_improved(df):
    x = df.columns[2]
    improved_fig = px.histogram(df, x=x, nbins=4)
    return improved_fig


def display_line_chart(df):
    df = pd.read_csv('pireas.csv')
    etos = df.columns[0] #['Winter', 'Spring', 'Summer', 'Fall']
    x = df[etos].to_list()

    name = df.columns[1]
    pireas = df[name].to_list()

    name = df.columns[2]
    thes = df[name].to_list()

    name = df.columns[3]
    patras = df[name].to_list()

    print('pireas is % and thes is %', pireas, thes)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name='ΕΚ Πειραιά',
        x=x, y=pireas,
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        name='ΕΚ Θεσσαλονίκη',
        x=x, y=thes,
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        name='ΕΚ Πάτρα',
        x=x, y=patras,
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))
    fig.update_layout(yaxis_range=(0, 3000))
    return fig


def single_line():
    dff = pd.read_csv('pireas.csv')
    fig = px.line(dff, x="Ετος", y="ΕΚ Πειραιά")
    fig.add_scatter(x=dff["Ετος"], y=dff["Thessaloniki"], mode='lines+markers')
    fig.add_scatter(x=dff["Ετος"], y=dff["ΕΚ Πάτρα"], mode='lines+text')
    fig.update_layout(yaxis_range=(0, 3000))
    return fig


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Συλλογή Ερευνητικών Εργασιών'),
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
        },
        id='datatable-interactivity',
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
    ),
    html.Div(id='datatable-interactivity-container'),
    # dcc.Dropdown(
    #     id='names', 
    #     value='Είδος Εργασίας', 
    #     options=[{'value': x, 'label': x} 
    #              for x in ['Είδος Εργασίας', 'Όνομα', 'Χρονιά']],
    #     clearable=False
    # ),
    #dcc.Graph(id="pie-chart"),
    # more babis here. just charts
    html.P("Κατανομή εργασιών στον χρόνο"),
    dcc.Graph(id="datespan_graph", figure=display_datespan_improved(df)),
    #dcc.Graph(id="datespan_graph",
    #          figure=display_datespan_graph(df)),
        html.Div([
        html.Div([
            html.H3('Διαδραστική Πίτα'),
            dcc.Dropdown(
        id='names', 
        value='Είδος Εργασίας', 
        options=[{'value': x, 'label': x} 
                 for x in ['Είδος Εργασίας', 'Όνομα', 'Χρονιά']],
        clearable=False
    ),
            dcc.Graph(id="pie-chart")
        ], className="six columns"),

        html.Div([
            html.H3('Κατηγορίες Ετών σε Στήλη'),
            dcc.Graph(id="datespan_graph2",
              figure=display_datespan_graph(df))
            #dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            html.H3('Line Chart cumulative'),
            dcc.Graph(id="linechart_graph", figure=display_line_chart(df))
        ], className="six columns"),

        html.Div([
            html.H3('Line chart'),
            dcc.Graph(id="lcg-cumulative",
              figure=single_line())
            #dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),
    ], className="row"),
    
    #html.H2("Line charts"),
    #dcc.Graph(id="linechart_graph", figure=display_line_chart(df)),
])


@app.callback(
    Output("pie-chart", "figure"), 
    [Input("names", "value")])
def generate_chart(names):
    fig = px.pie(df, names=names)
    return fig

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
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
                        "x": dff["Χρονιά"],
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
        for column in ["Είδος Εργασίας", "Όνομα"] if column in dff
        #for column in df.columns if column in dff
    ]
    return all_vs_all

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
app.css.config.serve_locally=False

if __name__ == '__main__':
    app.run_server(debug=True)