import dash
import dash_html_components as html
import dash_core_components as dcc

from utils.callbacks import *

app = dash.Dash(__name__)

slider_marks = {str(d): str(d) for d in range(32)}
slider_marks[0] = 'March'
app.layout = html.Div([
    # Header
    html.H1("Time-varying Data Visualization"),
    html.H2("Paris WI-FI"),
    # Day Slider, The project only need the data of march
    dcc.Slider(
        id='day-slider',
        min=0,
        max=31,
        value=0,
        marks=slider_marks,
        step=None,
        included=False
    ),
    # figures
    html.Div([
        # map
        html.Div(dcc.Graph(id='paris-wifi-map', config={'displayModeBar': False}), className='col-6'),
        # map choropleth
        html.Div(dcc.Graph(id='paris-wifi-choropleth', config={'displayModeBar': False}), className='col-6'),
    ], className='row'),

    html.Div([
        # polar bar daily
        html.Div(dcc.Graph(id='paris-wifi-polarBar', config={'displayModeBar': False}), className='col-6'),
        # polar bar hourly
        html.Div(dcc.Graph(id='paris-wifi-polarBar-hourly', config={'displayModeBar': False}), className='col-6'),
    ], className='row'),
    # Device distribution dropdown
    dcc.Dropdown(
        id='dropdown_device',
        options=[
            {'label': 'Device type', 'value': 'TYP'},
            {'label': 'Device constructer', 'value': 'CON'},
        ],
        value='TYP'
    ),
    html.Div([
        # distribution map
        html.Div(
            dcc.Graph(id='paris-wifi-device', config={'displayModeBar': False}), className='col-12'),
    ], className='row'),
], className='container')

# get all callbacks functions
get_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
