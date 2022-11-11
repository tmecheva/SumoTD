import header
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import pandas as pd
'''    
def CalculateResult(cfg):
    OutTree = ET.parse(header.simulation_path+'out.xml')
    dfOut=pd.DataFrame(columns = ["Detector","Time","qPKWcalc"])
    root=OutTree.getroot()
    for child in root.iter():
        d=child.get('id')
        t=child.get('begin')
        q=child.get('nVehEntered')            
        if t is not None and q is not None:
            t = int(float(t)/60)
            q=int(q)
            row = {'Detector':d,'Time':t,'qPKWcalc':q}
            dfOut=dfOut.append(row,ignore_index = True)

    dfIn = pd.read_csv(os.path.join(header.config_path,cfg+'.csv'),sep=";")
    res = pd.merge(dfOut,dfIn,on=["Detector","Time"],how="inner",validate="one_to_one").fillna(-1)
    Diff = pd.DataFrame({'Diff' : []})
    Diff=res['qPKWcalc']-res['qPKW']
    res['Pow']=Diff.pow(2)
    res.to_csv(os.path.join(header.result_path,cfg+'.csv'),index=False)   
'''

def CalculateErrors(cfg):
    DFin = CalculateInFlow(os.path.join(header.config_path,cfg+'.csv'))
    result=pd.DataFrame(columns = ["Configuration","Error"])
    subfolders = [f.path for f in os.scandir(os.path.join(header.result_path,cfg)) if f.is_dir()]
    for fol in subfolders:
        print(os.path.basename(fol))
        DFout = CalculateOutFlow(os.path.join(fol,'out.xml'))
        if not DFout.empty:
            ErrDF = pd.merge(DFout,DFin,on=["Detector","Time"],how="inner")
            ErrDF['Error']=ErrDF['qPKWsim']-ErrDF['qPKW']
            ErrDF['devisor']=ErrDF['qPKW'].replace([0],1)
            ErrDF['divisible']=ErrDF['Error'].abs()
            ErrDF['ErrorP']=ErrDF['divisible'].div(ErrDF['devisor'].values)
            meanError = ErrDF['ErrorP'].mean()
            #meanPowError = ErrDF['ErrorPow'].mean()
            row = pd.DataFrame(data={'Configuration':os.path.basename(fol),'Error':meanError},index=[0])
            result = pd.concat([result,row],ignore_index = True)
            #print(result)
    result.to_csv(os.path.join(header.result_path,'ErResult.csv'))
            
def CalculateInFlow(f):
    dfIn = pd.read_csv(f,sep=";")
    return dfIn[["Detector","Time","qPKW"]]

def CalculateOutFlow(f):    
    try:
        OutFlow = ET.parse(f)
        root=OutFlow.getroot()
        dfOut=pd.DataFrame(columns = ["Detector","Time","qPKWsim"])        
        for child in root.iter():
            d=child.get('id')
            t=child.get('begin')
            q=child.get('nVehEntered')            
            if t is not None and q is not None:
                t = int(float(t)/60)
                q=int(q)
                row = pd.DataFrame(data={'Detector':d,'Time':t,'qPKWsim':q},index=[0])
                dfOut=pd.concat([dfOut,row],ignore_index = True)
        return dfOut

    except ParseError:
        print("Simulation filliour", os.path.split(os.path.split(f)[0])[1])
        return pd.DataFrame()

CalculateErrors("ErrorsH")


    
