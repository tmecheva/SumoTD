import pandas as pd
import numpy as np
import os
import header
from datetime import datetime, date

class ControllerReport:
    def __init__(self,path,junction):
        self.junction=junction
        self.hdf=[pd.DataFrame(columns=['Detector'])]*24
        self.wdf=[pd.DataFrame(columns=['Detector'])]*24

        self.detectors=[]
        self.num=[]
        self.timestamp=[]
        self.df = pd.DataFrame()
        subfolders= [f.path for f in os.scandir(path) if f.is_dir()]

        for dirname in list(subfolders):
            if os.path.isfile(os.path.join(dirname,junction+'.xlsx')):
                print(os.path.join(dirname,junction+'.xlsx'))
                df1 = pd.read_excel(os.path.join(dirname,junction+'.xlsx'),header=[1])
                self.df = pd.concat([self.df, df1])
        #print(junction,'rows:',len(self.df.axes[0]),'cols:',self.df.axes[1])
        
        self.row=0
        self.df.drop([self.df.columns[1],self.df.columns[2],self.df.columns[5]], axis=1,inplace=True)
        #self.df.rename(columns={df.columns[0]='Time',df.columns[1]='Detectors',df.columns[2]='Count'})
        #print(junction,'rows:',len(self.df.axes[0]),'cols:',self.df.axes[1])
        #print(self.df.head)
        '''
        for x in range(0,self.df.shape[0]):
            self.df.drop(self.df.index[x], axis=0,inplace=True)
            if str(self.df.iloc[x,0])=='Дата':
                self.df.drop(self.df.index[x], axis=0,inplace=True)
                break
        '''
        
        self.Time = datetime.strptime(self.df.iloc[0,0],"%d.%m.%Y %H:%M:%S")
        #print(self.Time)

    
    def WriteValues(self):
        values = pd.DataFrame(data={'Detector':self.detectors,'qPKW':self.num})
        values.set_index('Detector',inplace=True)        
        if self.Time.weekday() in [6,7] or self.Time.date == date(year=2021,day=30,month=4):# or self.Time.date == datetime.date(year=2021,month=5,day=3):
            self.hdf[self.Time.hour] = pd.merge(self.hdf[self.Time.hour],values,how="outer",left_index=True,right_index=True,suffixes=("",self.Time))
        else:
            self.wdf[self.Time.hour] = pd.merge(self.wdf[self.Time.hour],values,how="outer",left_index=True,right_index=True,suffixes=("",self.Time))
            
    def GetValues(self):
        while self.row < self.df.shape[0]:
            currTime=datetime.strptime(self.df.iloc[self.row,0],"%d.%m.%Y %H:%M:%S")
            if self.Time != currTime:
                #print(currTime)
                self.WriteValues()
                self.CleanValues()
            else:
                self.GetValue()                
                self.row +=1
        
    def CleanValues(self):
        self.Time = datetime.strptime(self.df.iloc[self.row,0],"%d.%m.%Y %H:%M:%S")
        self.detectors=[]
        self.num=[]
        self.timestamp=[]
        
    def WriteValuesToCSV(self,i):
        dfH=pd.DataFrame(index=self.hdf[i].index)
        dfW=pd.DataFrame(index=self.wdf[i].index)

        dfH['Time'] = i*60
        dfW['Time'] = i*60
        dfH['qPKW'] = self.hdf[i].mean(axis = 1).round(0) 
        dfW['qPKW'] = self.wdf[i].mean(axis = 1).round(0)
        dfH['vPKW'] = 13.9
        dfW['vPKW'] = 13.9
        
        dfH = dfH.dropna()
        dfW = dfW.dropna()
        #print(dfW)
        dfH.to_csv(os.path.join(header.config_path,'hCFG.csv'),mode='a',sep=';',header=False)
        dfW.to_csv(os.path.join(header.config_path,'wCFG.csv'),mode='a',sep=';',header=False)

    def GetValue(self):        
        det = self.df.iloc[self.row,1]
        val = self.df.iloc[self.row,2]
        t = self.df.iloc[self.row,0]
        if type(det) == int and int(det)%2 == 1:
            self.detectors.append(self.junction+':'+str(det))
            self.num.append(val)

def CreateConfigFiles():
    dfH=pd.DataFrame(columns=['Detector','Time','qPKW','vPKW'])
    dfW=pd.DataFrame(columns=['Detector','Time','qPKW','vPKW'])
    dfH.to_csv(os.path.join(header.config_path,'hCFG.csv'),mode='a',sep=';',index=False)
    dfW.to_csv(os.path.join(header.config_path,'wCFG.csv'),mode='a',sep=';',index=False)
        
    CRList = []
    for j in header.junctions:
        CRList.append(ControllerReport(header.reports_path,j))
    
    for cr in CRList:
        cr.GetValues()
        
    for i in range(0,24):
        for cr in CRList:
            cr.WriteValuesToCSV(i)
    
            
CreateConfigFiles()
        
                      
    
