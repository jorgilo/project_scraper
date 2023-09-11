import os
import pandas as pd

def append_to_csv(fpath, df):
    if (os.path.exists(fpath)):
        x=pd.read_csv(fpath)
    else :
        x=pd.DataFrame()

    dfNew=pd.concat([x,df])
    dfNew['var_perc'] = dfNew.groupby('titulo')['precio_dolar'].pct_change().mul(100).round(2)
    dfNew.to_csv(fpath,index=False)

def append_to_excel(fpath, df):
    if (os.path.exists(fpath)):
        x=pd.read_excel(fpath)
    else :
        x=pd.DataFrame()

    dfNew=pd.concat([x,df])
    dfNew['var_perc'] = dfNew.groupby('titulo')['precio_dolar'].pct_change().mul(100).round(2)
    dfNew.to_excel(fpath,index=False)