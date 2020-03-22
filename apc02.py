import pandas as pd
import io
import requests
from scipy import spatial

def prepare_data(data):
    data_pivoted=data.drop(['Province/State','Lat', 'Long'], axis=1)
    return data_pivoted.melt(id_vars=['Country/Region'], var_name='date')

def get_country_values(data):
    data=data.drop_duplicates(['Country/Region','value'])
    data=data[data['value']>0]
    return data.sort_values(by=['Country/Region','value'])[['Country/Region','value']]

def get_country(data,country):
    return data[data['Country/Region']==country]

jhu_url="https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Confirmed.csv&filename=time_series_2019-ncov-Confirmed.csv"
rcontent=requests.get(jhu_url).content
data=pd.read_csv(io.StringIO(rcontent.decode('utf-8')))

data=prepare_data(data)
data=get_country_values(data)

co_df=get_country(data,'Colombia')['value'].to_numpy()
size=co_df.size
es_df=get_country(data,'Spain')['value'].to_numpy()

print(co_df[:size],es_df[:size])

print(1 - spatial.distance.cosine(co_df[:size],es_df[:size]))
