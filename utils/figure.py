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
                            color_continuous_scale=px.colors.carto.Bluyl
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
    r, theta = np.mgrid[6.5:7:7j, 0:(360 / 7 * 6):7j]
    # take data of weeks in march from 03-02 to 03-29
    color = sess_counts[1:29]
    color = np.asarray(color)
    whitecolor = np.zeros(21, dtype=int)
    color = np.append(whitecolor, color)

    fig = px.bar_polar(
        r=r.ravel(),
        theta=theta.ravel(),
        color=color.ravel(),
        title="Radical Weekly Wifi Connection Periodic Viz",
        labels={1:"cool"},
        start_angle=360/14,

        #hover_name='site_name',
        #hover_data=['site_code', 'site_name', 'session_count'],
        color_continuous_scale=[
            "rgb(255, 255, 255)",
            "#fbe6c5","#f5ba98","#ee8a82","#dc7176","#c8586c","#9c3f5d","#70284a",
        ]  # color from px.colors.carto.Buryl
    )
    fig.update_traces(text=np.mgrid[6.5:7:7j])
    fig.update_layout(polar_bargap=0)

    return fig


def get_fig_polar_bar_hourly(df):
    """
    get the fig polar bar layout
    :param df:
    :return:
    """
    sess_counts = df.session_count.tolist()
    r, theta = np.mgrid[1:7:33j, 0:(360 / 24 * 23):24j]  #33*24
    # take data of hours
    color = sess_counts #24*31

    color = np.asarray(color)
    whitecolor = np.zeros(48, dtype=int)
    color = np.append(whitecolor, color)

    fig = px.bar_polar(
        r=r.ravel(),
        theta=theta.ravel(),
        color=color.ravel(),
        title="Radical Hourly Wifi Connection Periodic Viz",
        start_angle=360 / 48,
        color_continuous_scale=[
            "rgb(255, 255, 255)",
            "#fbe6c5","#f5ba98","#ee8a82","#dc7176","#c8586c","#9c3f5d","#70284a",
        ]  # color from px.colors.carto.Buryl
    )
    fig.update_layout(polar_bargap=0)

    return fig


def get_fig_dist(df):

    colors = px.colors.qualitative.Pastel
    colors.append(px.colors.qualitative.Prism)
    colors.append(px.colors.qualitative.Safe)
    fig = go.Figure()
    for column in df:
        fig.add_trace(go.Bar(
            y= df.index,
            x=df[column],
            name=column,
            orientation='h',
            marker_color=colors[df.columns.get_loc(column)]
        ))
    fig.update_yaxes(nticks = 31)
    fig.update_layout(barmode='stack', xaxis_title = 'Number of connections',yaxis_title = 'Date', height = 800)
    return fig