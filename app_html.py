from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd

# https://www.youtube.com/watch?v=WOWVat5BgM4&ab_channel=CharmingData

# incorporate data into app
# df = pd.read_csv('C:\\Users\\chirico\\Documents\\dash_test\\test_data_2.csv')
df = pd.read_csv('https://raw.githubusercontent.com/ChiricoTRT/deploy_test/main/test_data_2.csv')

all_options = {
    'impact_01_accessibility': ['Walking', 'Walking and cycling', 'Private car only'],
    'impact_02_sustainability': ['Low', 'Medium', 'High', 'Climate-neutral']
}

colors = {'light_blue': '#02ACE3',
          'dark_blue': '#0047A0'
          }

# Build your components
# app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
graph_co2_red = dcc.Graph(figure={})
graph_co2_ttw = dcc.Graph(figure={})

dropdown_graph_co2_type = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot'],
                                       value='Bar Plot',  # initial value displayed when page first loads
                                       clearable=False)

dropdown_graph_co2_ttw_type = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot', 'Bubble'],
                                           value='Bar Plot',
                                           clearable=False)

dropdown_city = dcc.Dropdown(options=['Brussels', 'Madrid'],
                             value='Brussels',
                             clearable=False
                             )
double_filter = dcc.RadioItems(list(all_options.keys()),
                               'impact_01_accessibility',
                               id='indicators-radio_L1'
                               )
cost_input = dcc.Input(id='cost-input', value='', type='number')

# Layout - HTML
app.layout = html.Div(children=[
    # title
    html.H1(
        children='Test with Dash',
        style={
            'textAlign': 'center',
            'color': colors['light_blue']
        }
    ),

    # subtitle
    html.Div(children='Subtitle', style={
        'textAlign': 'center',
        'color': colors['dark_blue']
    }),

    # logo
    html.Div(children=[
        html.Img(src=r'assets/civitas-muse-logo-whitepng.png', alt='caption', width=200)
    ], style={'textAlign': 'center'}),
    html.Br(),

    # dropdown for the city selection
    html.Div(children=[dropdown_city], style={'textAlign': 'center', 'width': '30%', 'margin': 'auto'}),
    html.Br(),
    html.Div([
        html.Div(children=[
            html.H2('CO2 reduction', style={'textAlign': 'center', 'color': colors['light_blue']}),
            graph_co2_red,
            dropdown_graph_co2_type
        ], style={'padding': 10, 'flex': 1}),
        html.Div(children=[
            html.H2('CO2 emissions (thank-to-wheel)', style={'textAlign': 'center', 'color': colors['light_blue']}),
            graph_co2_ttw,
            dropdown_graph_co2_ttw_type
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'}),

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
            html.H3('Cost of the policy:'),
            dbc.Row(dbc.Col([cost_input], width=6)),
            dbc.Row(id='cost-output'),
            html.Br(),
            html.Button("Download dataset", id='btn-download-csv'),
            dcc.Download(id='download-dataframe-csv')
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])


# Callback allows components to interact
# CALLBACK TO CUSTOMIZE THE CO2 GRAPH
@app.callback(
    Output(graph_co2_red, component_property='figure'),
    Input(dropdown_graph_co2_type, component_property='value'),
    Input(dropdown_city, component_property='value')
)
def update_graph(user_input, city_input):  # function arguments come from the component property of the Input
    df2 = df[df['city'] == city_input]
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df2, x="scenario", y="CO2_reduct", color="component")

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=df2, x="scenario", y="CO2_reduct", color="component",
                         symbol="component")

    return fig  # returned objects are assigned to the component property of the Output


# CALLBACK TO CUSTOMIZE THE CO2 GRAPH Tank to wheel
@app.callback(
    Output(graph_co2_ttw, component_property='figure'),
    Input(dropdown_graph_co2_ttw_type, component_property='value'),
    Input(dropdown_city, component_property='value')
)
def update_graph(user_input, city_input):  # function arguments come from the component property of the Input
    df2 = df[df['city'] == city_input]
    print(df2)
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df2, x="scenario", y="CO2_ttw", color="component")

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=df2, x="scenario", y="CO2_ttw", color="component",
                         symbol="component")
    elif user_input == 'Bubble':
        fig = px.scatter(data_frame=df2, x="scenario", y="CO2_ttw", color="component",
                         symbol="component", size="CO2_reduct")

    return fig  # returned objects are assigned to the component property of the Output


# CALLBACK TO CHOOSE THE IMPACTS (FIRST LEVEL MENU)
@app.callback(
    Output('level-radio_L2', 'options'),
    Input('indicators-radio_L1', 'value'))
def set_impacts_options(selected_level):
    return [{'label': i, 'value': i} for i in all_options[selected_level]]


# CALLBACK TO SET THE INDICATOR (SECOND LEVEL MENU)
@app.callback(
    Output('level-radio_L2', 'value'),
    Input('level-radio_L2', 'options'))
def set_indicator(available_options):
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
    return f'Final cost: {input_value * 2}'


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "my_df.csv")


# Run app
if __name__ == '__main__':
    # app.run_server(port=8053)
    app.run(debug=True)
