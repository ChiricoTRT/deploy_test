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
          'dark_blue': '#0047A0',
          'green': '#8DC650'
          }

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA]) #, suppress_callback_exceptions=True)
graph_co2_red = dcc.Graph(figure={})
graph_co2_ttw = dcc.Graph(figure={})

dropdown_graph_co2_type = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot'],
                                       value='Bar Plot',  # initial value displayed when page first loads
                                       clearable=False)

dropdown_graph_co2_ttw_type = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot', 'Bubble'],
                                           value='Bar Plot',
                                           clearable=False)

radio_tr_sys_index1_method = dcc.RadioItems(options=['Method 1', 'Method 2', 'Method 3'],
                                            value='Method 1',
                                            id='radio-tr-sys-index1')

dropdown_city = dcc.Dropdown(options=['Brussels', 'Madrid'],
                             value='Brussels',
                             clearable=False
                             )

double_filter = dcc.RadioItems(list(all_options.keys()),
                               'impact_01_accessibility',
                               id='indicators-radio_L1'
                               )
cost_input = dcc.Input(id='cost-input', value='', type='number')

header = html.Div(children=[
    # header
    html.H1(
        children='Test with Dash',
        style={'textAlign': 'center', 'color': colors['light_blue']}
    ),
    # subtitle
    html.Div(children='Subtitle', style={
        'textAlign': 'center',
        'color': colors['dark_blue']
    }),
    # logo
    html.Div(children=[
        html.Img(src=r'assets/civitas-muse-logo-whitepng.png', alt='caption', width=200)
    ], style={'textAlign': 'center'})
]
)

# Layout - HTML
app.layout = html.Div(children=[
    header,
    html.Br(),

    # transport system mode 1
    html.Div(children=[
        html.H2(children='Transport system - mode 1',
                style={
                    'textAlign': 'center',
                    'color': colors['light_blue']
                })
    ]),
    html.Div([
        # INDEX 1
        html.Div(children=[
            html.H2('Index 1', style={'textAlign': 'center', 'color': colors['dark_blue']}),
            radio_tr_sys_index1_method,
            html.Br(),
            html.Div(children=[
                    html.I(
                        "Please type the inputs."),
                    html.Br(),
                    dcc.Input(id="tr_sys_input1_stop_dist", type="number", placeholder="Stop distance", min=0.1,
                              style={'marginRight': '10px'}),
                    dcc.Input(id="tr_sys_input2_avg_speed", type="number", placeholder="Average speed",
                              style={'marginRight': '10px'}),
                    dcc.Input(id="tr_sys_input3_avg_stop_time", type="number", placeholder="Average stop time",
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                    dcc.Input(id="tr_sys_input4_n_stop", type="number", placeholder="# stops",
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                    dcc.Input(id="tr_sys_input5_pt_speed", type="number", placeholder="PT speed",
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                    html.Div(id="tr_sys_output", style={'color': colors['light_blue'], 'fontSize': '14', 'fontWeight': 'bold'}),
                ]
            ),
        ], style={'padding': 10, 'flex': 1}),
        # INDEX 2
        html.Div(children=[
            html.H2('Index 2', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        ], style={'padding': 10, 'flex': 1}),
        # INDEX 3
        html.Div(children=[
            html.H2('Index 3', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    html.Br(),
    html.Hr(),
    html.Br(),

    # Indicators with tabs
    html.Div(children=[
        html.H2(children='Transport System',
                style={'textAlign': 'center', 'color': colors['light_blue']}
                )
    ]),
    html.Div([
        # TRANSPORT INDICATOR 1: PT SPEED
        html.Div(children=[
            html.H2('Public Transport Speed', style={'textAlign': 'center', 'color': colors['dark_blue']}),
            html.Div(children=[
                html.Div([
                    dcc.Tabs(id='tabs-tr-sys', value='tab-1', children=[
                        dcc.Tab(label='Method 1', value='tab-1'),
                        dcc.Tab(label='Method 2', value='tab-2'),
                        dcc.Tab(label='Method 3', value='tab-3')
                    ]),
                    html.Div(id='tabs-tr-sys-content')
                ]),
            ]
            ),
        ], style={'padding': 10, 'flex': 1}),
        # INDEX 2
        html.Div(children=[
            html.H2('Index 2', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        ], style={'padding': 10, 'flex': 1}),
        # INDEX 3
        html.Div(children=[
            html.H2('Index 3', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'}),


    # -----------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------

    # dropdown for the city selection
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Div(children=[dropdown_city], style={'textAlign': 'center', 'width': '30%', 'margin': 'auto'}),
    html.Br(),

    # two graphs
    html.Div([
        html.Div(children=[
            html.H2('CO2 reduction', style={'textAlign': 'center', 'color': colors['green']}),
            graph_co2_red,
            dropdown_graph_co2_type
        ], style={'padding': 10, 'flex': 1}),
        html.Div(children=[
            html.H2('CO2 emissions (thank-to-wheel)', style={'textAlign': 'center', 'color': colors['green']}),
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
# CALLBACK FOR INDEX 1 OF TRANSPORT SYSTEM, METHOD 1
@app.callback(
    Output("tr_sys_output", "children"),
    Output("tr_sys_input1_stop_dist", "required"),
    Output("tr_sys_input2_avg_speed", "required"),
    Output("tr_sys_input3_avg_stop_time", "required"),
    Output("tr_sys_input4_n_stop", "required"),
    Output("tr_sys_input5_pt_speed", "required"),
    Input("tr_sys_input1_stop_dist", "value"),
    Input("tr_sys_input2_avg_speed", "value"),
    Input("tr_sys_input3_avg_stop_time", "value"),
    Input("tr_sys_input4_n_stop", "value"),
    Input("tr_sys_input5_pt_speed", "value"),
    Input('radio-tr-sys-index1', 'value')
)
def update_output(stop_dist, avg_speed, avg_stop_time, n_stop, pt_speed, method):
    stop_dist_req = False
    avg_speed_req = False
    avg_stop_time_req = False
    n_stop_req = False
    pt_speed_req = False
    # TODO: add disable mode
    if method == 'Method 1':
        # change requirements
        stop_dist_req = True
        avg_speed_req = True
        avg_stop_time_req = True
        n_stop_req = True

        # calc
        if stop_dist is not None and avg_speed is not None and avg_stop_time is not None and n_stop is not None:
            score_calc = stop_dist / avg_speed * 60 * avg_stop_time * n_stop
            string_return = f'Score: {score_calc}'
        else:
            string_return = f''
    else:
        pt_speed_req = True
        if pt_speed is not None:
            score_calc = pt_speed
            string_return = f'Score: {score_calc}',
        else:
            string_return = f''
    return string_return, stop_dist_req, avg_speed_req, avg_stop_time_req, n_stop_req, pt_speed_req


# CALLBACK FOR TABS OF TRANSPORT SYSTEM INDICATORS
@app.callback(
    Output('tabs-tr-sys-content', 'children'),
    Input('tabs-tr-sys', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(children=[
            html.H2("Method 1"),
            html.I("Please fill with the input values"),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Div('Stop distance [km]', style={'margin-top': '10px'})),
                dbc.Col(
                    dcc.Input(id="stop_dist", type="number", placeholder="Stop distance", min=0.1,
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                ),
            ]),
            dbc.Row([
                dbc.Col(html.Div('Average speed [km/h]', style={'margin-top': '10px'})),
                dbc.Col(
                    dcc.Input(id="avg_speed", type="number", placeholder="Average speed", min=1,
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                ),
            ]),
            dbc.Row([
                dbc.Col(html.Div('Average stop time [min]', style={'margin-top': '10px'})),
                dbc.Col(
                    dcc.Input(id="avg_stop_time", type="number", placeholder="Average stop time", min=1,
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                ),
            ]),
            dbc.Row([
                dbc.Col(html.Div('Number of stops', style={'margin-top': '10px'})),
                dbc.Col(
                    dcc.Input(id="n_stop", type="number", placeholder="# stops", min=1,
                              style={'marginRight': '10px', 'margin-top': '10px'}),
                ),
            ]),
            html.Br(),
            html.Br(),
            html.Div(id="pt-speed_output"),
        ]
        ),
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, 10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, 10, 6],
                        type='bar'
                    )]
                )
            )
        ])


@app.callback(
    Output("pt-speed_output", "children"),
    Output("pt-speed_output", "style"),
    Input("stop_dist", "value"),
    Input("avg_speed", "value"),
    Input("avg_stop_time", "value"),
    Input("n_stop", "value"),
)
def update_output_tab(stop_dist, avg_speed, avg_stop_time, n_stop):
    # calc
    if stop_dist is not None and avg_speed is not None and avg_stop_time is not None and n_stop is not None:
        score_calc = stop_dist / avg_speed * 60 * avg_stop_time * n_stop
        string_return = f'Score: {score_calc}'
        style_ret = {'color': colors['light_blue'], 'fontSize': '16', 'fontWeight': 'bold'}
    else:
        string_return = f'Please fill all the input fields'
        style_ret = {'color': 'red'}

    return string_return, style_ret


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
