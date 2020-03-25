from google.cloud import storage

import pandas as pd
import numpy as np
import io
import requests
import json

#Get INS data and store it in BQ
FILE='data.json'

def get_data():
    url="https://atlas.jifo.co/api/connectors/aba1c676-18d4-40e6-adf6-b734905b12e2"
    s=requests.get(url).content
    return json.loads(s)

data=get_data()
dataframe=data['data'][2]
dataframe=pd.DataFrame(np.array(dataframe[1:]),columns=dataframe[0])
print(dataframe)

#Get JHU data and store it in BQ