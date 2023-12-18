from dash import html

layout_comp = {}

colors = {'light_blue': '#02ACE3',
          'dark_blue': '#0047A0',
          'green': '#8DC650'
          }

# ----------------------------------------------------------------------------------------
# --------------------------------------- HEADER -----------------------------------------
# ----------------------------------------------------------------------------------------
layout_comp['header'] = html.Div(children=[
    # header
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
    ], style={'textAlign': 'center'})
]
)
