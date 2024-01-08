import base64
import datetime
import io
from dash import Dash, dcc, Output, Input, html, State, dash_table  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd
from layout_components import *
from dash.exceptions import PreventUpdate

# https://www.youtube.com/watch?v=WOWVat5BgM4&ab_channel=CharmingData

# incorporate data into app
df = pd.read_csv('https://raw.githubusercontent.com/ChiricoTRT/deploy_test/main/test_data_2.csv')
sample_pt_speed = pd.read_csv('https://raw.githubusercontent.com/ChiricoTRT/deploy_test/main/Routes.csv')

# ----------------------------------------------------------------------------------------------------
# ------------------------------------- BUILD YOUR COMPONENTS ----------------------------------------
# ----------------------------------------------------------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)

# --------------------------------------------------------------------------------------------
# -------------------------------------- LAYOUT - HTML ---------------------------------------
# --------------------------------------------------------------------------------------------
app.layout = html.Div(children=[
    header,

    # Public Transport Indicators Title
    html.Div(children=[
        html.H1(children='Transport System',
                style={'textAlign': 'center', 'color': colors['light_blue']}
                )
    ]),

    # TRANSPORT INDICATOR 1: PT SPEED
    html.Div(children=[
        html.H2('Public Transport Speed', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        html.Br(),
        dbc.Row([
            # left column for the calculation
            dbc.Col(html.Div(children=[
                html.Div([
                    dcc.Tabs(id='tabs-ptspeed', value='tab-1-ptspeed', children=[
                        dcc.Tab(label='Method 1', value='tab-1-ptspeed'),
                        dcc.Tab(label='Method 2', value='tab-2-ptspeed'),
                        dcc.Tab(label='Method 3', value='tab-3-ptspeed')
                    ]),
                    html.Div(id='tabs-ptspeed-content')
                ]),
            ]), width=10,
            ),
            # right column for the score card
            dbc.Col(html.Div(children=[
                card_pt_system_ptspeed_body
            ]), width=2,
                style={'textAlign': 'center', 'border': 'none'},
                align='center'
            ),
        ]),
    ], style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Hr(),
    html.Br(),

    # TRANSPORT INDICATOR 2: ALTERNATIVE TO PRIVATE MEANS OF TRANSPORT
    html.Div(children=[
        html.H2('Alternative to private car index', style={'textAlign': 'center', 'color': colors['dark_blue']}),
        html.Br(),
        dbc.Row([
            # left column for the calculation
            dbc.Col(html.Div(children=[
                html.Div([
                    dcc.Tabs(id='tabs-nocar', value='tab-1-nocar', children=[
                        dcc.Tab(label='Local', value='tab-1-nocar', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Whole City', value='tab-2-nocar', style=tab_style, selected_style=tab_selected_style),
                    ]),
                    html.Div(id='tabs-nocar-content')
                ]),
            ]), width=10,
            ),
            # right column for the score card
            dbc.Col(html.Div(children=[
                card_pt_system_nocar_body
            ]), width=2,
                    style={'textAlign': 'center', 'border': 'none'},
                    align='center'
                    ),
        ]),
    ], style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Br(),

    # next section separator
    html.Hr(),
    html.Br(),
    html.Br(),

    # SOCIETY
    html.Div(children=[
        html.H1(children='Society',
                style={'textAlign': 'center', 'color': colors['light_blue']}
                )
    ]),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),
    # ECONOMY
    html.Div(children=[
        html.H1(children='Economy',
                style={'textAlign': 'center', 'color': colors['light_blue']}
                )
    ]),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),
    # RESULTS
    html.Div(children=[
        html.H1(children='Results',
                style={'textAlign': 'center', 'color': colors['light_blue']}
                ),
        dbc.Row([
            dbc.Col([card_pt_system_ptspeed_results]),
            dbc.Col([card_pt_system_nocar_results]),
        ]),
    ]),
    footer,
])


# CALLBACK FOR TABS OF TRANSPORT SYSTEM INDICATORS - PT SPEED
@app.callback(
    Output('tabs-ptspeed-content', 'children'),
    Input('tabs-ptspeed', 'value')
)
def render_content(tab):
    if tab == 'tab-1-ptspeed':
        return html.Div(children=[
            html.Br(),
            html.H2('Method 1'),
            html.Br(),
            dbc.Col([
                html.Div('Description here',
                         style={
                             'width': '100%',
                             'height': '60px',
                             'lineHeight': '60px',
                             'borderStyle': 'solid',
                             'borderColor': colors['light_blue'],
                             'textAlign': 'center',
                             'background-color': 'white',
                             'borderRadius': '2px',
                             'borderWidth': '1px',
                         }
                         ),
            ], style={'textAlign': 'center'}),
            html.Br(),
            html.I('If the city has a complex routing system, you can upload a csv file:'),
            html.Br(),
            html.Br(),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            id='upload-data-pt-sys-m1',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'background-color': 'white',
                                'borderColor': colors['light_blue'],
                                'color': colors['light_blue'],
                                'fontWeight': 'bold'
                            },
                        ),
                    ]),
                    dbc.Col([
                        dcc.Download(id='download-sample-ptspeed-m1'),
                        html.Button('Download sample dataset', id='btn-download-sample-ptspeed-m1',
                                    style={
                                        'width': '80%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderStyle': 'none',
                                        'textAlign': 'center',
                                        'background-color': 'white',
                                        'color': colors['dark_blue'],
                                        'fontWeight': 'bold'
                                    }),
                    ], style={'textAlign': 'center'}),
                    dbc.Col([
                        dcc.Store(id='memory-ptspeed'),
                        html.Button('Save', id='btn-save-ptspeed-m1', disabled=True,
                                    style={
                                        'width': '30%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderStyle': 'none',
                                        'textAlign': 'center',
                                        'background-color': 'grey',
                                        'color': 'white',
                                        'borderRadius': '10px',
                                        'fontWeight': 'bold'
                                    }),
                    ], style={'textAlign': 'center'}),
                ]),
                html.Br(),
                html.H3(id='title_pt_speed_res-ptspeed-m1', style={'textAlign': 'center', 'color': colors['light_blue']}),
                html.H1(id='pt-speed_output-score-file-ptspeed-m1',
                        style={
                            'textAlign': 'center',
                            'fontWeight': 'bold',
                            'color': colors['green']
                        }),
            ]),
            html.Br(),
            html.I('Otherwise, if the city has up to 5 routes, please fill with the input values below:'),
            html.Br(),
            # collapse
            html.Div(
                [
                    html.Br(),
                    dbc.Button(
                        'Show/hide input format',
                        id='collapse-button-ptspeed-m1',
                        className='mb-3',
                        n_clicks=0,
                        style={
                            'borderStyle': 'none',
                            'background-color': colors['light_blue'],
                            'color': 'white',
                            'fontWeight': 'bold'
                        }
                    ),
                    dbc.Collapse(children=[
                        input_5_routes_pt_speed_m1,
                        html.Br(),
                        html.Br(),
                        html.Div(id='pt-speed_output-ptspeed-m1-tabs'),
                        html.Br(),
                        html.H3(id='title_pt_speed_res-ptspeed-m1-tabs', style={'textAlign': 'center', 'color': colors['light_blue']}),
                        html.H1(id='pt-speed_output-score-ptspeed-m1-tabs',
                                style={'textAlign': 'center', 'fontWeight': 'bold', 'color': colors['green']}),
                        dbc.Col([
                            dcc.Store(id='memory-ptspeed'),
                            html.Button('Save', id='btn-save-ptspeed-m1-tabs', disabled=True,
                                        style={
                                            'width': '10%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderStyle': 'none',
                                            'textAlign': 'center',
                                            'background-color': 'grey',
                                            'color': 'white',
                                            'borderRadius': '10px',
                                            'fontWeight': 'bold'
                                        }),
                        ], style={'textAlign': 'center'}),
                    ],
                        id='collapse-ptspeed-m1-tabs',
                        is_open=False,
                    ),
                ]
            ),
        ]
        ),
    elif tab == 'tab-2-ptspeed':
        return html.Div([
            html.Br(),
            html.H2('Method 2'),
            html.Br(),
            dbc.Col([
                html.Div('Description here',
                         style={
                             'width': '100%',
                             'height': '60px',
                             'lineHeight': '60px',
                             'borderStyle': 'solid',
                             'borderColor': colors['light_blue'],
                             'textAlign': 'center',
                             'background-color': 'white',
                             'borderRadius': '2px',
                             'borderWidth': '1px',
                         }
                         ),
            ], style={'textAlign': 'center'}),
            html.Br(),
            html.I('Please fill the inputs:'),
            html.Br(),
            dcc.Input(id='measured-time-min-ptspeed-m2', type='number', placeholder='Measured time (min)', min=1,
                      style={'marginRight': '10px', 'margin-top': '10px'}),
            dcc.Input(id='measured-time-sec-ptspeed-m2', type='number', placeholder='Measured time (sec)', min=0,
                      max=59,
                      style={'marginRight': '10px', 'margin-top': '10px'}),
            html.Button('Add', id='measured-time-confirm-ptspeed-m2',
                        style={
                            'width': '10%', 'height': '60px', 'lineHeight': '60px', 'borderStyle': 'none',
                            'textAlign': 'center', 'background-color': 'grey', 'color': 'white',
                            'borderRadius': '10px', 'fontWeight': 'bold', 'marginRight': '10px'
                        }),
            html.Button('Reset', id='measured-time-reset-ptspeed-m2', disabled=True,
                        style={
                            'width': '10%', 'height': '60px', 'lineHeight': '60px', 'borderStyle': 'none',
                            'textAlign': 'center', 'background-color': 'grey', 'color': 'white',
                            'borderRadius': '10px', 'fontWeight': 'bold', 'marginRight': '10px'
                        }
                        ),
            html.Br(),
            html.I('Added values:'),
            html.Br(),
            html.Div([], id='ptspeed-m2-out-list'),
            html.Br(),
            html.H3('', id='ptspeed-m2-res-title',
                    style={'textAlign': 'center', 'color': colors['light_blue']}),
            html.H1(id='ptspeed-m2-result',
                    style={
                        'textAlign': 'center',
                        'fontWeight': 'bold',
                        'color': colors['green']
                    }),
            html.Br(),
            dbc.Col([
                dcc.Store(id='memory-ptspeed'),
                html.Button('Save', id='btn-save-ptspeed-m2', disabled=True,
                            style={
                                'width': '10%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderStyle': 'none',
                                'textAlign': 'center',
                                'background-color': 'grey',
                                'color': 'white',
                                'borderRadius': '10px',
                                'fontWeight': 'bold'
                            }),
            ], style={'textAlign': 'center'}),
        ])
    elif tab == 'tab-3-ptspeed':
        return html.Div([
            html.Br(),
            html.H2('Method 3'),
            html.Br(),
            dbc.Col([
                html.Div('Description here',
                         style={
                             'width': '100%',
                             'height': '60px',
                             'lineHeight': '60px',
                             'borderStyle': 'solid',
                             'borderColor': colors['light_blue'],
                             'textAlign': 'center',
                             'background-color': 'white',
                             'borderRadius': '2px',
                             'borderWidth': '1px',
                         }
                         ),
            ], style={'textAlign': 'center'}),
            html.Br(),
            html.I('Please upload a csv file:'),
            html.Br(),
            html.Br(),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            id='upload-data-pt-sys-m3',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'background-color': 'white',
                                'borderColor': colors['light_blue'],
                                'color': colors['light_blue'],
                                'fontWeight': 'bold'
                            },
                        ),
                    ]),
                    dbc.Col([
                        dcc.Download(id='download-sample-ptspeed-m3'),
                        html.Button('Download sample dataset', id='btn-download-sample-ptspeed-m3',
                                    style={
                                        'width': '80%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderStyle': 'none',
                                        'textAlign': 'center',
                                        'background-color': 'white',
                                        'color': colors['dark_blue'],
                                        'fontWeight': 'bold'
                                    }),
                    ], style={'textAlign': 'center'}),
                    dbc.Col([
                        dcc.Store(id='memory-ptspeed'),
                        html.Button('Save', id='btn-save-ptspeed-m3', disabled=True,
                                    style={
                                        'width': '30%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderStyle': 'none',
                                        'textAlign': 'center',
                                        'background-color': 'grey',
                                        'color': 'white',
                                        'borderRadius': '10px',
                                        'fontWeight': 'bold'
                                    }),
                    ], style={'textAlign': 'center'}),
                ]),
                html.Br(),
                html.H3(id='title_pt_speed_res-ptspeed-m3', style={'textAlign': 'center', 'color': colors['light_blue']}),
                html.H1(id='pt-speed_output-score-file-ptspeed-m3',
                        style={
                            'textAlign': 'center',
                            'fontWeight': 'bold',
                            'color': colors['green']
                        }),
            ]),
        ])


@app.callback(
    Output('ptspeed-m2-result', 'children', allow_duplicate=True),
    Output('ptspeed-m2-out-list', 'children', allow_duplicate=True),
    Input('measured-time-reset-ptspeed-m2', 'n_clicks'),
    prevent_initial_call=True
)
def reset_pt_sys_m2(n_clicks):
    if n_clicks:
        result = ''
        added_list = []

    return result, added_list


@app.callback(Output('ptspeed-m2-out-list', 'children', allow_duplicate=True),
              Output('measured-time-confirm-ptspeed-m2', 'disabled'),
              Output('measured-time-confirm-ptspeed-m2', 'style'),
              Output('measured-time-min-ptspeed-m2', 'value'),
              Output('measured-time-sec-ptspeed-m2', 'value'),
              Output('measured-time-confirm-ptspeed-m2', 'n_clicks'),
              Output('ptspeed-m2-result', 'children', allow_duplicate=True),
              Output('ptspeed-m2-res-title', 'children'),
              Output('btn-save-ptspeed-m2', 'disabled', allow_duplicate=True),
              Output('btn-save-ptspeed-m2', 'style'),
              Output('measured-time-reset-ptspeed-m2', 'disabled'),
              Input('ptspeed-m2-out-list', 'children'),
              Input('measured-time-min-ptspeed-m2', 'value'),
              Input('measured-time-sec-ptspeed-m2', 'value'),
              Input('measured-time-confirm-ptspeed-m2', 'n_clicks'),
              Input('ptspeed-m2-result', 'children'),
              prevent_initial_call=True)
def add_measured_time(out_value, mins, secs, n_click, result):
    reset_btn_disable = True
    if len(out_value) > 0:
        reset_btn_disable = False

    btn_disabled = True
    btn_style = {'width': '10%', 'height': '60px', 'lineHeight': '60px', 'borderStyle': 'none',
                 'textAlign': 'center', 'background-color': 'grey', 'color': 'white',
                 'borderRadius': '10px', 'fontWeight': 'bold', 'marginRight': '10px'
                 }

    if mins is not None or secs is not None:
        btn_disabled = False
        btn_style = {'width': '10%', 'height': '60px', 'lineHeight': '60px', 'borderStyle': 'none',
                     'textAlign': 'center', 'background-color': colors['green'], 'color': 'white',
                     'borderRadius': '10px', 'fontWeight': 'bold', 'marginRight': '10px'
                     }
    if n_click:
        reset_val_min = None
        reset_val_sec = None
        btn_disabled = True
        n_click = None
        reset_btn_disable = False
        btn_style = {'width': '10%', 'height': '60px', 'lineHeight': '60px', 'borderStyle': 'none',
                     'textAlign': 'center', 'background-color': 'grey', 'color': 'white',
                     'borderRadius': '10px', 'fontWeight': 'bold', 'marginRight': '10px'
                     }
        if mins is not None and secs is not None:
            out_value.append(round(mins + secs / 60, 2))
            out_value.append(' | ')
        if mins is not None and secs is None:
            out_value.append(round(mins, 2))
            out_value.append(' | ')
        if mins is None and secs is not None:
            out_value.append(round(secs / 60, 2))
            out_value.append(' | ')
        tmp = []
        for r in out_value:
            if r != ' | ':
                tmp.append(r)
        result = round(sum(tmp) / len(tmp), 2)

    else:
        reset_val_min = mins
        reset_val_sec = secs
    if result is not None:
        title = 'Public Transport Speed Score'
        save_disable = False
        save_style = {
            'width': '10%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': colors['green'],
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold',
            'marginRight': '10px'
        }
    else:
        title = ''
        save_disable = True
        save_style = {
            'width': '10%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': 'grey',
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }

    return out_value, btn_disabled, btn_style, reset_val_min, reset_val_sec, n_click, result, title, \
           save_disable, save_style, reset_btn_disable


@app.callback(Output('pt-speed_output-score-file-ptspeed-m1', 'children'),
              Output('title_pt_speed_res-ptspeed-m1', 'children'),
              Output('btn-save-ptspeed-m1', 'style'),
              Output('btn-save-ptspeed-m1', 'disabled'),
              Input('upload-data-pt-sys-m1', 'contents'))
def update_output(contents):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    pt_speed = round(
        (df['stop_distance_km'] / df['average_speed_km_h'] * 60 + (df['average_stop_time_min'] * df['numbers_of_stops'])).mean(), 2)

    btn_disabled = True
    btn_style = {}

    if contents:
        title = 'Public Transport Speed Score'
        btn_style = {
            'width': '30%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': colors['green'],
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }
        btn_disabled = False
    else:
        title = ''

    return pt_speed, title, btn_style, btn_disabled


@app.callback(Output('pt-speed_output-score-file-ptspeed-m3', 'children'),
              Output('title_pt_speed_res-ptspeed-m3', 'children'),
              Output('btn-save-ptspeed-m3', 'style'),
              Output('btn-save-ptspeed-m3', 'disabled'),
              Input('upload-data-pt-sys-m3', 'contents'))
def update_output(contents):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    pt_speed = round(
        (df['stop_distance_km'] / df['average_speed_km_h'] * 60 + (df['average_stop_time_min'] * df['numbers_of_stops'])).mean(), 2)

    btn_disabled = True
    btn_style = {}

    if contents:
        title = 'Public Transport Speed Score'
        btn_style = {
            'width': '30%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': colors['green'],
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }
        btn_disabled = False
    else:
        title = ''

    return pt_speed, title, btn_style, btn_disabled


@app.callback(
    Output('pt-speed_output-ptspeed-m1-tabs', 'children'),
    Output('pt-speed_output-ptspeed-m1-tabs', 'style'),
    Output('pt-speed_output-score-ptspeed-m1-tabs', 'children'),
    Output('title_pt_speed_res-ptspeed-m1-tabs', 'children'),
    Output('btn-save-ptspeed-m1-tabs', 'style'),
    Output('btn-save-ptspeed-m1-tabs', 'disabled'),
    Input('stop_dist_1', 'value'),
    Input('stop_dist_2', 'value'),
    Input('stop_dist_3', 'value'),
    Input('stop_dist_4', 'value'),
    Input('stop_dist_5', 'value'),
    Input('avg_speed_1', 'value'),
    Input('avg_speed_2', 'value'),
    Input('avg_speed_3', 'value'),
    Input('avg_speed_4', 'value'),
    Input('avg_speed_5', 'value'),
    Input('avg_stop_time_1', 'value'),
    Input('avg_stop_time_2', 'value'),
    Input('avg_stop_time_3', 'value'),
    Input('avg_stop_time_4', 'value'),
    Input('avg_stop_time_5', 'value'),
    Input('n_stop_1', 'value'),
    Input('n_stop_2', 'value'),
    Input('n_stop_3', 'value'),
    Input('n_stop_4', 'value'),
    Input('n_stop_5', 'value'),
)
def update_output_tab(stop_dist_1, stop_dist_2, stop_dist_3, stop_dist_4, stop_dist_5,
                      avg_speed_1, avg_speed_2, avg_speed_3, avg_speed_4, avg_speed_5,
                      avg_stop_time_1, avg_stop_time_2, avg_stop_time_3, avg_stop_time_4, avg_stop_time_5,
                      n_stop_1, n_stop_2, n_stop_3, n_stop_4, n_stop_5
                      ):
    # calc
    score_calc_1 = None
    score_calc_2 = None
    score_calc_3 = None
    score_calc_4 = None
    score_calc_5 = None

    style_1 = 'normal'
    style_2 = 'normal'
    style_3 = 'normal'
    style_4 = 'normal'
    style_5 = 'normal'

    m = ''
    title = ''
    btn_disabled = True
    btn_style = {
        'width': '10%',
        'height': '60px',
        'lineHeight': '60px',
        'borderStyle': 'none',
        'textAlign': 'center',
        'background-color': 'grey',
        'color': 'white',
        'borderRadius': '10px',
        'fontWeight': 'bold'
    }

    if stop_dist_1 is not None and avg_speed_1 is not None and avg_stop_time_1 is not None and n_stop_1 is not None:
        score_calc_1 = round(stop_dist_1 / avg_speed_1 * 60 * avg_stop_time_1 * n_stop_1, 5)
        style_1 = 'bold'

    if stop_dist_2 is not None and avg_speed_2 is not None and avg_stop_time_2 is not None and n_stop_2 is not None:
        score_calc_2 = round(stop_dist_2 / avg_speed_2 * 60 * avg_stop_time_2 * n_stop_2, 2)
        style_2 = 'bold'

    if stop_dist_3 is not None and avg_speed_3 is not None and avg_stop_time_3 is not None and n_stop_3 is not None:
        score_calc_3 = round(stop_dist_3 / avg_speed_3 * 60 * avg_stop_time_3 * n_stop_3, 2)
        style_3 = 'bold'

    if stop_dist_4 is not None and avg_speed_4 is not None and avg_stop_time_4 is not None and n_stop_4 is not None:
        score_calc_4 = round(stop_dist_4 / avg_speed_4 * 60 * avg_stop_time_4 * n_stop_4, 2)
        style_4 = 'bold'

    if stop_dist_5 is not None and avg_speed_5 is not None and avg_stop_time_5 is not None and n_stop_5 is not None:
        score_calc_5 = round(stop_dist_5 / avg_speed_5 * 60 * avg_stop_time_5 * n_stop_5, 2)
        style_5 = 'bold'

    if score_calc_1 or score_calc_2 or score_calc_3 or score_calc_4 or score_calc_5:
        # mean of valid arguments
        m = 0
        c = 0
        for sc in [score_calc_1, score_calc_2, score_calc_3, score_calc_4, score_calc_5]:
            if sc is not None:
                c += 1
                m += sc
        m = m / c
        title = 'Public Transport Speed Score'
        btn_disabled = False
        btn_style = {
            'width': '10%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': colors['green'],
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }

        string_return = dbc.Col([
            html.Div(f'Score R1: {score_calc_1}', style={'margin-top': '10px', 'fontWeight': style_1}),
            html.Div(f'Score R2: {score_calc_2}', style={'margin-top': '10px', 'fontWeight': style_2}),
            html.Div(f'Score R3: {score_calc_3}', style={'margin-top': '10px', 'fontWeight': style_3}),
            html.Div(f'Score R4: {score_calc_4}', style={'margin-top': '10px', 'fontWeight': style_4}),
            html.Div(f'Score R5: {score_calc_5}', style={'margin-top': '10px', 'fontWeight': style_5}),
        ]),
        style_ret = {'color': colors['light_blue'], 'fontSize': '16'}
    else:
        string_return = f'Please fill at least all the input fields of one route'
        style_ret = {'color': 'red'}

    return string_return, style_ret, m, title, btn_style, btn_disabled


@app.callback(
    Output('download-sample-ptspeed-m1', 'data'),
    Input('btn-download-sample-ptspeed-m1', 'n_clicks'),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(sample_pt_speed.to_csv, 'sample_pt_speed.csv')


@app.callback(
    Output('download-sample-ptspeed-m3', 'data'),
    Input('btn-download-sample-ptspeed-m3', 'n_clicks'),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(sample_pt_speed.to_csv, 'sample_pt_speed.csv')


@app.callback(
    Output('collapse-ptspeed-m1-tabs', 'is_open'),
    [Input('collapse-button-ptspeed-m1', 'n_clicks')],
    [State('collapse-ptspeed-m1-tabs', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('memory-ptspeed', 'data', allow_duplicate=True),
    Output('btn-save-ptspeed-m1', 'n_clicks'),
    Input('btn-save-ptspeed-m1', 'n_clicks'),
    Input('pt-speed_output-score-file-ptspeed-m1', 'children'),
    prevent_initial_call=True
)
def save_pt_sys(n_click, score):
    if n_click is None:
        raise PreventUpdate
    else:
        n_click_reset = None

    return score, n_click_reset


@app.callback(
    Output('memory-ptspeed', 'data', allow_duplicate=True),
    Output('btn-save-ptspeed-m1-tabs', 'n_clicks'),
    Input('btn-save-ptspeed-m1-tabs', 'n_clicks'),
    Input('pt-speed_output-score-ptspeed-m1-tabs', 'children'),
    prevent_initial_call=True
)
def save_pt_sys(n_click, score):
    if n_click is None:
        raise PreventUpdate
    else:
        n_click_reset = None

    return score, n_click_reset


@app.callback(
    Output('memory-ptspeed', 'data', allow_duplicate=True),
    Output('btn-save-ptspeed-m2', 'n_clicks'),
    Input('btn-save-ptspeed-m2', 'n_clicks'),
    Input('ptspeed-m2-result', 'children'),
    prevent_initial_call=True
)
def save_pt_sys(n_click, score):
    if n_click is None:
        raise PreventUpdate
    else:
        n_click_reset = None

    return score, n_click_reset


@app.callback(
    Output('memory-ptspeed', 'data', allow_duplicate=True),
    Output('btn-save-ptspeed-m3', 'n_clicks'),
    Input('btn-save-ptspeed-m3', 'n_clicks'),
    Input('pt-speed_output-score-file-ptspeed-m3', 'children'),
    prevent_initial_call=True
)
def save_pt_sys(n_click, score):
    if n_click is None:
        raise PreventUpdate
    else:
        n_click_reset = None

    return score, n_click_reset


@app.callback(
    Output('transport-score-body', 'children'),
    Input('memory-ptspeed', 'data'),
)
def update_transport_card_body(data):
    if data is None:
        raise PreventUpdate

    return data


@app.callback(
    Output('transport-score-results', 'children', allow_duplicate=True),
    Input('memory-ptspeed', 'data'),
    prevent_initial_call=True
)
def update_transport_card_results(data):
    if data is None:
        raise PreventUpdate

    return data


@app.callback(
    Output('nocar-score-body', 'children'),
    Input('memory-nocar', 'data'),
)
def update_nocar_card_body(data):
    if data is None:
        raise PreventUpdate

    return data


@app.callback(
    Output('nocar-score-results', 'children'),
    Input('memory-nocar', 'data'),
)
def update_nocar_card_body(data):
    if data is None:
        raise PreventUpdate

    return data


# CALLBACK FOR TABS OF TRANSPORT SYSTEM INDICATORS
@app.callback(
    Output('tabs-nocar-content', 'children'),
    Input('tabs-nocar', 'value')
)
def render_content(tab):
    if tab == 'tab-1-nocar':
        return html.Div(children=[
            html.Br(),
            html.H2('Local experiment'),
            html.Br(),
            dbc.Col([
                html.Div('Description here',
                         style={
                             'width': '100%',
                             'height': '60px',
                             'lineHeight': '60px',
                             'borderStyle': 'solid',
                             'borderColor': colors['light_blue'],
                             'textAlign': 'center',
                             'background-color': 'white',
                             'borderRadius': '2px',
                             'borderWidth': '1px',
                         }
                         ),
            ], style={'textAlign': 'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div('Inhabitants',
                                         style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='inhab-nocar-loc', type='number', placeholder='Inhabitants', min=1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Public Transport Length [km]',
                                         style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='pt-length-nocar-loc', type='number', placeholder='PT Length (km)', min=1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Average days of PT service',
                                         style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='pt-day-serv-nocar-loc', type='number', placeholder='PT service days', min=1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Number of PT stops',
                                         style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='pt-stops-nocar-loc', type='number', placeholder='PT stops number', min=1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Share of PT cost on income',
                                         style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='pt-cost-nocar-loc', type='number', placeholder='Share of PT cost', min=0.1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Beta-1 parameter', style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='beta-1-nocar-loc', type='number', placeholder='Beta-1 param (optional)',
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        ),
                        dbc.Tooltip(children=([
                            html.Div('Beta 1 parameter is optional. '
                                     'Default value is 1. It can be used to boost the PT length weight in the formula.',
                                     style={'color': 'white', 'fontSize': '0.8vw', 'textAlign': 'left'}
                                     )
                        ]),
                            target='beta-1-nocar-loc',
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Beta-2 parameter', style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='beta-2-nocar-loc', type='number', placeholder='Beta-2 param (optional)',
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        ),
                        dbc.Tooltip(children=([
                            html.Div('Beta 2 parameter is optional. '
                                     'Default value is 1. It can be used to boost the average days of service weight in the formula.',
                                     style={'color': 'white', 'fontSize': '0.8vw', 'textAlign': 'left'}
                                     )
                        ]),
                            target='beta-2-nocar-loc',
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Beta-3 parameter', style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='beta-3-nocar-loc', type='number', placeholder='Beta-3 param (optional)',
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        ),
                        dbc.Tooltip(children=([
                            html.Div('Beta 3 parameter is optional. '
                                     'Default value is 0.5. It can be used to boost the number of stops weight in the formula.',
                                     style={'color': 'white', 'fontSize': '0.8vw', 'textAlign': 'left'}
                                     )
                        ]),
                            target='beta-3-nocar-loc',
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div('Beta-4 parameter', style={'margin-top': '10px', 'fontWeight': 'bold'}
                                         ), width=5),
                        dbc.Col(
                            dcc.Input(id='beta-4-nocar-loc', type='number', placeholder='Beta-4 param (optional)', max=-0.1,
                                      style={'marginRight': '10px', 'margin-top': '10px'}),
                        ),
                        dbc.Tooltip(children=([
                            html.Div('Beta 4 parameter is optional. '
                                     'Default value is -1. It can be used to boost the share of PT cost weight in the formula. '
                                     'Only negative values are allowed.',
                                     style={'color': 'white', 'fontSize': '0.8vw', 'textAlign': 'left'}
                                     )
                        ]),
                            target='beta-4-nocar-loc',
                        ),
                    ]),
                ]),
                dbc.Col([
                    html.H3(id='title_nocar-loc', style={'textAlign': 'center', 'color': colors['light_blue']}),
                    html.H1(id='nocar-local-output',
                            style={
                                'textAlign': 'center',
                                'fontWeight': 'bold',
                                'color': colors['green']
                            }),
                    dcc.Store(id='memory-nocar'),
                    dbc.Row([
                        dbc.Col("", width=4),
                        dbc.Col([
                            html.Button('Save', id='btn-save-nocar-local', disabled=True,
                                        style={
                                            'width': '100%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderStyle': 'none',
                                            'textAlign': 'center',
                                            'background-color': 'grey',
                                            'color': 'white',
                                            'borderRadius': '10px',
                                            'fontWeight': 'bold'
                                        }),
                        ], width=4),
                    ], align='center'),
                ], align='center')
            ]),
        ])

    elif tab == 'tab-2-nocar':
        return html.Div([
            html.Br(),
            html.H2('Whole city experiment'),
            html.Br(),
            dbc.Col([
                html.Div('Description here',
                         style={
                             'width': '100%',
                             'height': '60px',
                             'lineHeight': '60px',
                             'borderStyle': 'solid',
                             'borderColor': colors['light_blue'],
                             'textAlign': 'center',
                             'background-color': 'white',
                             'borderRadius': '2px',
                             'borderWidth': '1px',
                         }
                         ),
            ], style={'textAlign': 'center'}),
        ])


@app.callback(
    Output('title_nocar-loc', 'children'),
    Output('nocar-local-output', 'children'),
    Output('btn-save-nocar-local', 'style'),
    Output('btn-save-nocar-local', 'disabled'),
    Input('inhab-nocar-loc', 'value'),
    Input('pt-length-nocar-loc', 'value'),
    Input('pt-day-serv-nocar-loc', 'value'),
    Input('pt-stops-nocar-loc', 'value'),
    Input('pt-cost-nocar-loc', 'value'),
    Input('beta-1-nocar-loc', 'value'),
    Input('beta-2-nocar-loc', 'value'),
    Input('beta-3-nocar-loc', 'value'),
    Input('beta-4-nocar-loc', 'value'),
)
def compute_output_nocar_local(inhab, pt_len, pt_day_serv, pt_stops, pt_cost, beta1, beta2, beta3, beta4):
    title = ""
    score = ""
    btn_disabled = True

    # enable or not the calculation
    show_result = False
    count = 0
    mandatory_inp = [inhab, pt_len, pt_day_serv, pt_stops, pt_cost]
    for mi in mandatory_inp:
        if mi is not None:
            count += 1
    if count / len(mandatory_inp) == 1:
        show_result = True

    # check beta values and assign default is empty
    if beta1 is None:
        beta1 = 1
    if beta2 is None:
        beta2 = 1
    if beta3 is None:
        beta3 = 0.5
    if beta4 is None:
        beta4 = -1

    if show_result:
        title = "Alternatives to car score"
        score = round(
            ((pt_len**beta1) * (pt_day_serv**beta2) * (pt_stops**beta3) * (pt_cost**beta4)) / inhab,
            2)
        btn_style = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': colors['green'],
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }
        btn_disabled = False
    else:
        btn_style = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderStyle': 'none',
            'textAlign': 'center',
            'background-color': 'grey',
            'color': 'white',
            'borderRadius': '10px',
            'fontWeight': 'bold'
        }

    return title, score, btn_style, btn_disabled


@app.callback(
    Output('memory-nocar', 'data', allow_duplicate=True),
    Output('btn-save-nocar-local', 'n_clicks'),
    Input('btn-save-nocar-local', 'n_clicks'),
    Input('nocar-local-output', 'children'),
    prevent_initial_call=True
)
def save_nocar_loc(n_click, score):
    if n_click is None:
        raise PreventUpdate
    else:
        n_click_reset = None
        print(score)

    return score, n_click_reset


# Run app
if __name__ == '__main__':
    # app.run_server(port=8053)
    app.run(debug=True)
