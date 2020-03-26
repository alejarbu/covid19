import pandas as pd
import io
import requests
from scipy import spatial
from sklearn.cluster import KMeans
import numpy as np

COUNTRY='Country/Region'

OFFSET=8
K=4

def get_data(local=True):
    def get_online_data():
        jhu_url="https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
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
    c_array = []
    c_names = []
    for c in countries:
        t_df=get_country(data,c)
        c_names.append(c)
        c_array.append(t_df[:size])
    
    return c_names, c_array

def get_countries(data,country):
        size=get_country(data,country).size+OFFSET
        return data.groupby(COUNTRY).filter(lambda x: len(x) > size)[COUNTRY].unique()

data = get_data(local=False)
data = process_data(data)

c_names, X = get_similar(data,'Colombia',get_countries(data,'Colombia'))
kmeans = KMeans(n_clusters=K, random_state=0).fit(X)

kmodel = pd.DataFrame({'country':c_names, 'cluster':kmeans.labels_, 'data':X})
col=get_country(data,'Colombia')
pred=kmeans.predict([col])

print(c_names)
print(kmeans.cluster_centers_)
print(kmodel)
print(col)
print(kmodel[kmeans.labels_==pred])