import plotly.express as px
import config.auth as config


def get_fig_map(df):
    """
    get the fig map layout
    :param df:
    :return:
    """
    fig = px.scatter_mapbox(df,
                            lon='lon',
                            lat='lat',
                            size='session_count',
                            color='session_count',
                            title='test title',
                            hover_name='site_name',
                            hover_data=['site_code', 'site_name', 'session_count'],
                            color_continuous_scale=px.colors.carto.Temps
                            )

    fig.update_layout(
        mapbox={'accesstoken': config.MAP_BOX_TOKEN, 'center': {'lat': 48.853499, 'lon': 2.3493147}, 'zoom': 11},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    return fig
