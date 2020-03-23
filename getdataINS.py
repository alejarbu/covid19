import pandas as pd
import numpy as np
import io
import requests
import json

FILE='data.json'

def get_data(local=False):
    if local:
        with open(FILE) as f:
            data = json.load(f)
    else:
        url="https://atlas.jifo.co/api/connectors/aba1c676-18d4-40e6-adf6-b734905b12e2"
        s=requests.get(url).content
        data=json.loads(s)
        with open(FILE, 'w') as outfile:
            json.dump(data, outfile)

    return data

data=get_data(local=True)
dataframe=data['data'][2]
dataframe=pd.DataFrame(np.array(dataframe[1:]),columns=dataframe[0])
print(dataframe)
