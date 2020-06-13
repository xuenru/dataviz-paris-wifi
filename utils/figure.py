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


def get_fig_polar_bar(df):
    """
    get the fig polar bar layout
    :param df:
    :return:
    """
    sess_counts = df.session_count.tolist()
    r, theta = np.mgrid[1:7:7j, 0:(360 / 7 * 6):7j]
    # take data of weeks in march from 03-02 to 03-29
    color = sess_counts[1:29]
    color = np.asarray(color)
    whitecolor = np.zeros(21, dtype=int)
    color = np.append(whitecolor, color)

    fig = px.bar_polar(
        r=r.ravel(),
        theta=theta.ravel(),
        color=color.ravel(),
        color_continuous_scale=[
            "rgb(255, 255, 255)",
            "rgb(57, 177, 133)",
            "rgb(156, 203, 134)",
            "rgb(233, 226, 156)",
            "rgb(238, 180, 121)",
            "rgb(232, 132, 113)",
            "rgb(207, 89, 126)",
        ]  # color from px.colors.carto.Temps
    )
    fig.update_layout(polar_bargap=0)

    return fig
