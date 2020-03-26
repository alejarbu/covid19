import pandas as pd
import io
import requests

COUNTRY='Country/Region'
PATH='local/data/'

jhu_confirmed_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
jhu_recovered_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
jhu_deaths_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def get_online_data(url,filename):
        rcontent=requests.get(url).content
        data=pd.read_csv(io.StringIO(rcontent.decode('utf-8')))
        data=data.drop(['Province/State','Lat', 'Long'], axis=1)
        data=data.melt(id_vars=[COUNTRY], var_name='date')
        data.to_csv(PATH+filename,index=False)
        print(filename)
        print(data)
        return data

get_online_data(jhu_confirmed_url,'jhu_confirmed.csv')
get_online_data(jhu_recovered_url,'jhu_recovered.csv')
get_online_data(jhu_deaths_url,'jhu_deaths.csv')
