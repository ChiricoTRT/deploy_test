from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd

# https://www.youtube.com/watch?v=WOWVat5BgM4&ab_channel=CharmingData

# incorporate data into app
# df = px.data.medals_long()
df = pd.read_csv('C:\\Users\\chirico\\Documents\\dash_test\\test_data_2.csv')

all_options = {
    'impact_01_accessibility': ['Walking', 'Walking and cycling', 'Private car only'],
    'impact_02_sustainability': ['Low', 'Medium', 'High', 'Climate-neutral']
}

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot'],
                        value='Bar Plot',  # initial value displayed when page first loads
                        clearable=False)
double_filter = dcc.RadioItems(list(all_options.keys()),
                               'impact_01_accessibility',
                               id='indicators-radio_L1'
                               )
cost_input = dcc.Input(id='cost-input', value='', type='number')

# Layout - HTML
app.layout = html.Div(children=[
    html.H1(
        children='Test with Dash',
        style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    html.Div(children='Subtitle.', style={
        'textAlign': 'center',
        'color': '#7FDBFF'
    }),
    html.Div(children=[
        html.Img(src=r'assets/civitas-muse-logo-whitepng.png', alt='caption', width=100)
    ], style={'textAlign': 'center'}),
    html.Br(),
    mygraph,
    dropdown,
    html.Div([
        html.Div(children=[
            html.H2('Left hand side'),
            html.Br(),
            double_filter,
            html.Br(),
            dcc.RadioItems(id='level-radio_L2'),
            html.Br(),
            dbc.Row(id='display-selected-values'),
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            html.H2('Right hand side'),
            html.Br(),
            dbc.Row(dcc.Markdown('## Cost of the policy:')),
            dbc.Row(dbc.Col([cost_input], width=6)),
            dbc.Row(id='cost-output')
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])


# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df, x="scenario", y="CO2_reduct", color="component")

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=df, x="scenario", y="CO2_reduct", color="component",
                         symbol="component")

    return fig  # returned objects are assigned to the component property of the Output


@app.callback(
    Output('level-radio_L2', 'options'),
    Input('indicators-radio_L1', 'value'))
def set_cities_options(selected_level):
    return [{'label': i, 'value': i} for i in all_options[selected_level]]


@app.callback(
    Output('level-radio_L2', 'value'),
    Input('level-radio_L2', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('indicators-radio_L1', 'value'),
    Input('level-radio_L2', 'value'))
def set_display_children(selected_level, selected_city):
    return f'{selected_city} is a level for {selected_level}'


@app.callback(
    Output(component_id='cost-output', component_property='children'),
    Input(component_id='cost-input', component_property='value')
)
def update_output_cost(input_value):
    return f'Final cost: {input_value*2}'


# Run app
if __name__ == '__main__':
    # app.run_server(port=8053)
    app.run(debug=True)
