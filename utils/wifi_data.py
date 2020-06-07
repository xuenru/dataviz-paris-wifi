import pandas as pd


def get_df_full():
    """
    get all the date from csv
    :return: DataFrame
    """
    df = pd.read_csv("./data/paris-wi-fi-utilisation-des-hotspots-paris-wi-fi.csv", sep=";",
                     usecols=["Code Site", "Date heure début", "Nom du site", "geo_point_2d"]).dropna()
    df[['lat', 'lon']] = df.geo_point_2d.str.split(",", expand=True)
    df = df.drop(['geo_point_2d'], axis=1)
    df.columns = ['site_code', 'session_date', 'site_name', 'lat', 'lon']
    df.session_date = pd.to_datetime(df.session_date, utc=True).dt.date
    return df.astype({'session_date': 'datetime64[ns]', 'lat': float, 'lon': float})


def get_df_period(df, from_date, to_date):
    """
    get df filtered by date
    :param df: pd.DataFrame
    :param from_date: Y-m-d
    :param to_date: Y-m-d
    :return: pd.DataFrame
    """
    mask = (df.session_date >= from_date) & (df.session_date <= to_date)
    return df[mask]


def get_df_nb_sess(df):
    """
    get df with count of session
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    tmp = df.groupby(['site_code', 'site_name', 'lat', 'lon']).count()
    tmp.columns = ['session_count']
    return tmp.reset_index()


def get_df_period_nb_sess(df, from_date, to_date):
    """
    get df for map figure
    :param df: pd.DataFrame
    :param from_date: Y-m-d
    :param to_date: Y-m-d
    :return: pd.DataFrame
    """
    return get_df_nb_sess(get_df_period(df, from_date, to_date))
