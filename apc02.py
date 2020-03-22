import pandas as pd
import io
import requests
from scipy import spatial

COUNTRY='Country/Region'

def get_data(local=True):
    def get_online_data():
        jhu_url="https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Confirmed.csv&filename=time_series_2019-ncov-Confirmed.csv"
        rcontent=requests.get(jhu_url).content
        data=pd.read_csv(io.StringIO(rcontent.decode('utf-8')))
        data=data.drop(['Province/State','Lat', 'Long'], axis=1)
        data=data.melt(id_vars=[COUNTRY], var_name='date')
        data.to_csv('jhu_data.csv',index=False)
        return data

    if local:
        return pd.read_csv('jhu_data.csv')
    else:
        return get_online_data()

def process_data(data):
    data=data.drop_duplicates([COUNTRY,'value'])
    data=data[data['value']>0]
    return data.sort_values(by=[COUNTRY,'value'])[[COUNTRY,'value']]

def get_country(data,country):
        return data[data[COUNTRY]==country]['value'].to_numpy()

def get_similar(data,country,countries):
    o_df=get_country(data,country)
    size=o_df.size
    print(country,o_df)
    for c in countries:
        t_df=get_country(data,c)[:size]
        print(c,",",1 - spatial.distance.cosine(o_df,t_df),",",t_df)

def get_countries(data,country):
        size=get_country(data,country).size
        return data.groupby(COUNTRY).filter(lambda x: len(x) > size)[COUNTRY].unique()

data=get_data(local=True)
data=process_data(data)
#get_similar(data,'Colombia',['Spain','Italy'])
get_similar(data,'Colombia',get_countries(data,'Colombia'))