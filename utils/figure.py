import plotly.express as px
import config.auth as config
import numpy as np
import plotly.graph_objects as go


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


def get_fig_polarBar(df):
    """

    :param df:
    :return:
    """

    r, theta = np.mgrid[0.6:1:7j, 0:(360 / 8 * 7):7j]
    color = df
    #print(color)
    # color=[90, 51, 126, 164, 203, 232, 218, 182, 156, 121, 126, 45, 129, 117, 70, 66, 72, 93, 17, 10, 21, 20, 38, 72, 73, 44, 101, 88, 40, 18]
    #color = [16, 49, 85, 52, 75, 114, 22, 8, 55, 38, 61, 54, 50, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    color = np.asarray(color)
    whitecolor = np.zeros(14)
    color = np.append(whitecolor, color)

    fig = go.Figure(go.Barpolar(
        r=r.ravel(),
        theta=theta.ravel(),
        marker_color=color.ravel()), )
    fig.update_layout(polar_bargap=0, showlegend=False

                      )
    return fig
