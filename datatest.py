import pandas as pd

df = pd.read_csv("./data/paris-wi-fi-utilisation-des-hotspots-paris-wi-fi.csv", sep=";",
                 usecols=["Code Site", "Date heure début", "Nom du site", "geo_point_2d"]).dropna()
df[['lat', 'lon']] = df.geo_point_2d.str.split(",", expand=True)
df = df.drop(['geo_point_2d'], axis=1)
df.columns = ['site_code', 'session_date', 'site_name', 'lat', 'lon']
df['session_hour'] = pd.to_datetime(df.session_date, utc=True).dt.hour
df.session_date = pd.to_datetime(df.session_date, utc=True).dt.date

