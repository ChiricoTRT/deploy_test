from dash import html, dcc
import dash_bootstrap_components as dbc

colors = {'light_blue': '#02ACE3',
          'dark_blue': '#0047A0',
          'green': '#8DC650'
          }

# ----------------------------------------------------------------------------------------
# --------------------------------------- HEADER -----------------------------------------
# ----------------------------------------------------------------------------------------
header = html.Div(children=[
    # header
    html.Br(),
    html.Br(),
    html.H1(
        children='MUSE - Evaluation Framework',
        style={
            'textAlign': 'center',
            'color': colors['light_blue']
        }
    ),
    # subtitle
    html.Div(children='This tool is developed to calculate the indicators',
             style={
                 'textAlign': 'center',
                 'color': colors['dark_blue']
             }),
    # logo
    html.Br(),
    html.Br(),
    html.Div(children=[
        html.Img(src=r'assets/civitas-muse-logo-whitepng.png', alt='caption', width=200)
    ], style={'textAlign': 'center'})
]
)

footer = html.Div(children=[
    html.Br(),
    html.Hr(),
    html.Br(),
    # logo
    html.Div(children=[
        html.Img(src=r'assets/civitas-muse-logo-whitepng.png', alt='caption', width=200)
    ], style={'textAlign': 'center'}),
    html.Br(),
    html.H1(
        children='MUSE - Evaluation Framework',
        style={
            'textAlign': 'center',
            'color': colors['dark_blue']
        }
    ),
    html.Br(),
]
)


input_5_routes_pt_speed = html.Div([
    dbc.Row([
        dbc.Col(html.Div('Stop distance [km]', style={'margin-top': '10px', 'fontWeight': 'bold'})),
        dbc.Row([
            dbc.Col(
                dcc.Input(id="stop_dist_1", type="number", placeholder="Stop distance R1", min=0.1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="stop_dist_2", type="number", placeholder="Stop distance R2", min=0.1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="stop_dist_3", type="number", placeholder="Stop distance R3", min=0.1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="stop_dist_4", type="number", placeholder="Stop distance R4", min=0.1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="stop_dist_5", type="number", placeholder="Stop distance R5", min=0.1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
        ]),
    ]),
    dbc.Row([
        dbc.Col(html.Div('Average speed [km/h]', style={'margin-top': '10px', 'fontWeight': 'bold'})),
        dbc.Row([
            dbc.Col(
                dcc.Input(id="avg_speed_1", type="number", placeholder="Average speed R1", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_speed_2", type="number", placeholder="Average speed R2", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_speed_3", type="number", placeholder="Average speed R3", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_speed_4", type="number", placeholder="Average speed R4", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_speed_5", type="number", placeholder="Average speed R5", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
        ]),
    ]),
    dbc.Row([
        dbc.Col(html.Div('Average stop time [min]', style={'margin-top': '10px', 'fontWeight': 'bold'})),
        dbc.Row([
            dbc.Col(
                dcc.Input(id="avg_stop_time_1", type="number", placeholder="Average stop time R1", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_stop_time_2", type="number", placeholder="Average stop time R2", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_stop_time_3", type="number", placeholder="Average stop time R3", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_stop_time_4", type="number", placeholder="Average stop time R4", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="avg_stop_time_5", type="number", placeholder="Average stop time R5", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
        ]),
    ]),
    dbc.Row([
        dbc.Col(html.Div('Number of stops', style={'margin-top': '10px', 'fontWeight': 'bold'})),
        dbc.Row([
            dbc.Col(
                dcc.Input(id="n_stop_1", type="number", placeholder="R1 stops", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="n_stop_2", type="number", placeholder="R2 stops", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="n_stop_3", type="number", placeholder="R3 stops", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="n_stop_4", type="number", placeholder="R4 stops", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
            dbc.Col(
                dcc.Input(id="n_stop_5", type="number", placeholder="R5 stops", min=1,
                          style={'marginRight': '10px', 'margin-top': '10px'}),
            ),
        ]),
    ]),
])


# RESULTS CARDS
card_pt_system = dbc.Card(
    [
        dbc.CardImg(src=r'assets/transport.png', top=True),
        dbc.CardBody(
            [
                html.H4("Transport score", className="card-title", style={'textAlign': 'center'}),
                html.H2(id='transport-score', style={
                    'textAlign': 'center',
                    'color': colors['green']
                }),
            ]
        ),
    ],
    style={"width": "18rem"},
)
