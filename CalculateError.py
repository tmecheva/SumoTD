import header
import pandas as pd
import os
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import ParseError

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

def CalculateError(cfg):
    DFin = CalculateInFlow(os.path.join(header.config_path,cfg+'.csv'))
    result=pd.DataFrame(columns = ["Configuration","Error","PowError"])
    subfolders = [f.path for f in os.scandir(os.path.join(header.result_path,cfg)) if f.is_dir()]
    for fol in subfolders:
        print(os.path.basename(fol))
        DFout = CalculateOutFlow(os.path.join(fol,'out.xml'))
        if not DFout.empty:
            ErrDF = pd.merge(DFout,DFin,on=["Detector","Time"],how="inner")
            ErrDF['divisor'] = ErrDF['qPKW']
            ErrDF['divisor'].replace(to_replace = 0, value = 1, inplace=True)
            ErrDF['divisible'] = ErrDF['qPKWsim']-ErrDF['qPKW']
            ErrDF['Error']=(ErrDF['divisible'].abs()/ErrDF['divisor'])
            meanError = ErrDF['Error'].mean()
            row = pd.DataFrame(data={'Configuration':os.path.basename(fol),'Error':meanError},index=[0])
            result = pd.concat([result,row],ignore_index = True)
    result.to_csv(os.path.join(header.result_path,'ERresult.csv'))
    
CalculateError('hCFG')
