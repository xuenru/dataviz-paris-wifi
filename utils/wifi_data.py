import pandas as pd
import numpy as np


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
    df.session_date = pd.to_datetime(df.session_date, utc=True)

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


def get_df_nb_sess_with_info(df, site_code=None):
    """
    get df with count of session with site info
    :param df: pd.DataFrame
    :param site_code:
    :return: pd.DataFrame
    """
    tmp = df.groupby(['site_code', 'site_name', 'lat', 'lon']).count()
    tmp.columns = ['session_count']
    df_info = tmp.reset_index()

    return df_info if site_code is None else df_info[df_info.site_code == site_code]


def get_df_nb_sess(df, site_code=None, from_date='2020-03-01', nb_days=31):
    """
    get df with count of session
    :param df: pd.DataFrame
    :param site_code: if None for all the sites
    :param from_date: Y-m-d
    :param nb_days: int

    :return: tuple of pd.DataFrame
    """
    df_sel = df if site_code is None else df[df['site_code'] == site_code]
    # count session connections by hour
    hourly_count = pd.DataFrame({'session_count': [0] * nb_days * 24},
                                index=pd.date_range(from_date, periods=nb_days * 24, freq='H'))
    hc = df_sel.set_index('session_date').resample('H').count()
    hc['session_count'] = hc['site_code']
    hourly_count.loc[hc.index, 'session_count'] = hc.session_count.tolist()

    # count session connections by day
    daily_count = hourly_count.resample('D').sum()

    return daily_count, hourly_count


def get_df_period_nb_sess(df, from_date, to_date, with_info=False, site_code=None):
    """
    get df for map figure
    :param df: pd.DataFrame
    :param from_date: Y-m-d
    :param to_date: Y-m-d
    :param site_code: string
    :param with_info: if it has the site info
    :return: tuple of pd.DataFrame
    """
    df_period = get_df_period(df, from_date, to_date)

    return get_df_nb_sess_with_info(df_period, site_code) if with_info else get_df_nb_sess(df_period, site_code)


def get_df_dist():
    """
    get all the distribution data from csv
    :return: DataFrame
    """
    df = pd.read_csv("./data/paris-wi-fi-utilisation-des-hotspots-paris-wi-fi.csv", sep=";",
                        usecols=[ "Date heure début","Code postal", "Type d'appareil", "Constructeur appareil"]).dropna()
    df.columns = ['session_date', 'postal_code', 'device_type', 'device_mark']
    df.session_date = pd.to_datetime(df.session_date, utc=True)
    df = df.astype({'session_date': 'datetime64[ns]','postal_code': 'str'})
    df['postal_code']= df['postal_code'].astype(str)

    df_postal_code = df.drop(columns=['device_type', 'device_mark'])
    df_postal_code['count'] = 1
    df_postal_code = pd.DataFrame.pivot_table( df_postal_code, index = 'session_date', columns = ['postal_code'], values = ['count'], aggfunc = np.sum, fill_value=0)
    df_postal_code = df_postal_code.groupby(df_postal_code.index.date).sum().iloc[1:]

    df_device_type = df.drop(columns=['postal_code', 'device_mark'])
    df_device_type['count'] = 1
    df_device_type = pd.DataFrame.pivot_table( df_device_type, index = 'session_date', columns = ['device_type'], values = ['count'], aggfunc = np.sum, fill_value=0)
    df_device_type = df_device_type.groupby(df_device_type.index.date).sum().iloc[1:]

    df_device_mark = df.drop(columns=['postal_code', 'device_type'])
    df_device_mark['count'] = 1
    df_device_mark = pd.DataFrame.pivot_table( df_device_mark, index = 'session_date', columns = ['device_mark'], values = ['count'], aggfunc = np.sum, fill_value=0)
    df_device_mark = df_device_mark.groupby(df_device_mark.index.date).sum().iloc[1:]
    
    return df_postal_code, df_device_type, df_device_mark


def get_df_choropleth(df, from_date, to_date):
    """
    prepare df for paris district map
    :param df: DataFrame from get_df_dist()
    :param from_date: datetime
    :param to_date: datetime
    :return: DataFrame
    """
    df_period = df.loc[from_date.date():to_date.date()]
    df_period.columns = [int(p) + 100 for p in df_period.columns.get_level_values(1)]

    df_poste_total = df_period.transpose().sum(1).reset_index()
    df_poste_total.columns = ['postal_code', 'count']

    return df_poste_total
