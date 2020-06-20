from dash.dependencies import Input, Output
import pandas as pd
import utils.figure as fig
import utils.wifi_data as wd


def get_callbacks(app):
    df_full = wd.get_df_full()
    tuple_df_dist = tuple(wd.get_df_dist())

    # plot Map
    @app.callback(
        [Output('paris-wifi-map', 'figure'),
         Output('paris-wifi-choropleth', 'figure')],
        [Input('day-slider', 'value')])
    def update_graph(selected_day):
        if selected_day == 0:
            from_date = pd.datetime(2020, 3, 1, 0)
            to_date = pd.datetime(2020, 3, 31, 23)
        else:
            from_date = pd.datetime(2020, 3, selected_day, 0)
            to_date = pd.datetime(2020, 3, selected_day, 23)
        df = wd.get_df_period_nb_sess(df_full, from_date, to_date, with_info=True)
        df_choropleth = wd.get_df_choropleth(tuple_df_dist[0], from_date, to_date)

        return fig.get_fig_map(df), fig.get_fig_map_choropleth(df_choropleth)

    # plot distribution bar chart
    @app.callback(
        Output('paris-wifi-device', 'figure'),
        [Input('dropdown_device', 'value')])
    def dist_graph(dropdown):
        if dropdown == 'TYP':
            selected = 1
        elif dropdown == 'CON':
            selected = 2
        df = tuple_df_dist[selected]['count']
        return fig.get_fig_dist(df)

    # plot Polar Chart
    @app.callback(
        [Output('paris-wifi-polarBar', 'figure'),
         Output('paris-wifi-polarBar-hourly', 'figure'),
         Output('paris-wifi-3d', 'figure')],
        [Input('paris-wifi-map', 'clickData')])
    def update_wifi_site_selected(clickData):
        # data of march
        from_date = pd.datetime(2020, 3, 1, 0)
        to_date = pd.datetime(2020, 3, 31, 23)
        site_code = None if clickData is None else clickData['points'][0]['customdata'][0]

        df_daily, df_hourly = wd.get_df_period_nb_sess(df_full, from_date, to_date, site_code=site_code)

        return fig.get_fig_polar_bar(df_daily), fig.get_fig_polar_bar_hourly(df_hourly), fig.get_fig_3d_plot(df_hourly)
