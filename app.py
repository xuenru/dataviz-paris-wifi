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
        html.Div(dcc.Graph(id='paris-wifi-map', config={'displayModeBar': True}), className='col-8'),
        # TODO polar chart
        html.Div(dcc.Graph(id='paris-wifi-polarBar', config={'displayModeBar': True}), className='col-4'),
        #html.Div(html.Div(id="wifi-site-info"), className='col-4')
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
    Output('paris-wifi-polarBar', 'figure'),
    [Input('paris-wifi-map', 'clickData')])
def update_wifi_site_selected(clickData):
    if clickData == None:
        df = [7, 24, 46, 18, 17, 29, 65, 30, 58, 38, 65, 52, 51, 49, 66, 22, 16, 10, 14, 13, 2, 6, 7, 10, 6, 10, 8, 5, 3, 7]
        return fig.get_fig_polarBar(df)
    else:
        df = wd.get_df_period_nb_sess_site(df_full, clickData['points'][0]['customdata'][0])
        return fig.get_fig_polarBar(df)

if __name__ == '__main__':
    app.run_server(debug=True)
