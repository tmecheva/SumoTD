import pandas as pd
import ControllerReport as cr
import csv as csv
from datetime import date
import numpy as np
import random
import os

class InputFlows:
    def __init__(self,CFfile,CRpath):
        self.df = pd.read_csv(CFfile)
        self.path = CRpath
        self.Junctions = []


        for x in range(0,self.df.shape[0]):
            j = self.df.iloc[x,0]
            det = self.df.iloc[x,1]
            d = list(map(int, det.split()))
            CRfile= CRpath +'/'+str(j)+'.xlsx'

            CR = cr.ControllerReport(CRfile)
            self.Junctions.append({'Junction':j,'Detectors':d,'ControllerReport':CR})

    def ReadTimeInterval(self):
        is_not_EOF = True
        for i in range(0,len(self.Junctions)):
            if self.Junctions[i]['ControllerReport'].GetTimeInterval() == False:
                is_not_EOF = False
        
        for i in range(1,len(self.Junctions)):
            if self.Junctions[i]['ControllerReport'].Time != self.Junctions[i-1]['ControllerReport'].Time or is_not_EOF==False:
                return '';
        return self.Junctions[0]['ControllerReport'].Time;

    def WriteDetectrosTimeseries(self,path):
        TimeDF = pd.DataFrame(columns = ["Detector","Time","qPKW","vPKW"])
        file = path+'/'+'holidays.csv'
        TimeDF.to_csv(file,index=False,mode='w',sep=',')
        file = path+'/'+'workingdays.csv'
        TimeDF.to_csv(file,index=False,mode='w',sep=',')
        
        while 1:
            TimeDF = pd.DataFrame(columns = ["Detector","Time","qPKW","vPKW"])
            d = self.ReadTimeInterval()
            if d == '':
                return;

            for i in range(0,len(self.Junctions)):
                for v in self.Junctions[i]['ControllerReport'].values:
                    if v['detector'] in self.Junctions[i]['Detectors']:
                        j= str(self.Junctions[i]['Junction'])+':'+str(v['detector'])+"Din"
                        row = {'Detector':j,'Time':str(d.time().hour*60),'qPKW':v['value'],'vPKW':random.randrange(45,55)}
                        TimeDF=TimeDF.append(row,ignore_index = True)
        
            if d.weekday() in [5,6]:
                file = path+'/'+'holidays.csv'
            else:
                file = path+'/'+'workingdays.csv'
                
            TimeDF.to_csv(file,index=False,header=False,mode='a',sep=',')
            
    def CalculateFlowsCSV(self,infile,outfile):
        DF=pd.read_csv(infile)
        DF = DF.groupby(['Time','Detector']).mean().astype(int).reset_index().reindex(columns = ["Detector","Time","qPKW","vPKW"])
        DF.to_csv(outfile,mode='w',index = False,sep=';')           
        
    def CalculateFlowsByHourCSV(self,infile,outfile,hour):
        DF=pd.read_csv(infile)
        DF = DF[DF['Time']==hour*60].groupby(['Detector']).mean().astype(int).reset_index().reindex(columns = ["Detector","Time","qPKW","vPKW"])
        DF["Time"] = 0
        DF.to_csv(outfile,mode='w',index = False,sep=';')
