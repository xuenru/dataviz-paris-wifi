import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utils.figure as fig
import utils.wifi_data as wd

app = dash.Dash(__name__)

df_full = wd.get_df_full()
df = wd.get_df_nb_sess(df_full)

slider_marks = {str(d): str(d) for d in df_full.session_date.dt.day.unique()}
slider_marks[0] = 'Full month'
app.layout = html.Div([
    # Header
    html.H1("Paris WI-FI"),
    # Silder
    dcc.Slider(
        id='day-slider',
        min=0,
        max=df_full.session_date.max().day,
        value=0,
        marks=slider_marks,
        step=None
    ),
    # figures
    html.Div([
        # map
        html.Div(dcc.Graph(id='paris-wifi-map', config={'displayModeBar': False}), className='col-8'),
        # TODO polar chart
        html.Div(html.Div(id="wifi-site-info"), className='col-4')
    ], className='row'),
], className='container')


# plot Map
@app.callback(
    Output('paris-wifi-map', 'figure'),
    [Input('day-slider', 'value')])
def update_graph(selected_day):
    if selected_day == 0:
        from_date = "2020-03-01"
        to_date = "2020-03-31"
    else:
        from_date = to_date = "2020-03-" + str(selected_day)
    df = wd.get_df_period_nb_sess(df_full, from_date, to_date)
    return fig.get_fig_map(df)


# plot Polar Chart
@app.callback(
    Output('wifi-site-info', 'children'),
    [Input('paris-wifi-map', 'clickData')])
def update_wifi_site_selected(clickData):
    return "#######TODO Polar Chart:####### {}".format(str(clickData))


if __name__ == '__main__':
    app.run_server(debug=True)
