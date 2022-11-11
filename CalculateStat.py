import header
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import pandas as pd

    
def CalculateError(cfg):
    result = pd.DataFrame()
    for f in os.listdir(os.path.join(header.result_path,cfg)):
        df = pd.read_csv(os.path.join(header.result_path,cfg,f),sep=",")
        result = pd.concat([result,df],ignore_index = True)
        
    result[result['Error'] == result['Error'].min()].to_csv(os.path.join(header.result_path,'ErrorsH','minH.csv'))

    print('Total number: ',result['Error'].shape[0],'Min discrepancy number: ',result[result['Error'] == result['Error'].min()].shape[0],"Deviation : ",result['Error'].std(),"Minimum discrepancy: ",result['Error'].min())
    
def CalculateDeviation(f):
    df = pd.read_csv(f)
    print('deviation is ',df['Error'].std())
    print('min error is ',df['Error'].min())

#for cfg in header.configFiles:
CalculateDeviation("/home/tedy/Sumo/script/SumoTD/Result/wWagner_step01/wWagner_step001.csv")
#CalculateDeviation(os.path.join(header.result_path,'ErrorsH','Wid.csv'))
#CalculateError("ErrorsH")


    
