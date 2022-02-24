import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import paths

class OutputFlows:
    def __init__(self,input_cfg):
        self.OutTree = ET.parse(paths.simulation_path+'out.xml')

        self.dfIn = pd.read_csv(input_cfg,sep=";")
        self.path = paths.result_path
        self.dfOut=pd.DataFrame(columns = ["Detector","Time","qPKWcalc"])
    
        root=self.OutTree.getroot()
        for child in root.iter():
            d=child.get('id')
            t=child.get('begin')
            q=child.get('nVehEntered')            
            if t is not None and q is not None:
                t = int(float(t)/60)
                q=int(q)
                row = {'Detector':d,'Time':t,'qPKWcalc':q}
                self.dfOut=self.dfOut.append(row,ignore_index = True)
        
    def Compare(self):
        self.dfOut = self.dfOut.reindex(columns=['Detector','Time','qPKWcalc'])
        res = pd.merge(self.dfOut,self.dfIn,on=["Detector","Time"],how="inner",validate="one_to_one").fillna(-1)
        Diff = pd.DataFrame({'Diff' : []})
        Diff=res['qPKWcalc']-res['qPKW']
        res['Pow']=Diff.pow(2)
        res.to_csv(self.path,index=False)        
        return res['Pow'].mean()


        
                            
    
        
        
