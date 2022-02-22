import pandas as pd
import numpy as np
from datetime import datetime

class ControllerReport:
    def __init__(self,p):
        self.Time = ''
        self.path = p
        self.df = pd.read_excel(p)
        self.rows = self.df.shape[0]
        self.cols = self.df.shape[1]
        self.values = []
        self.XY = {
            "time":'',
            "direction":'',
            "detector":'',
            "value":0,
            "row":0
        }
        for x in range(0,self.rows):
            for y in range(0,self.cols):
                if self.df.iloc[x,y]=='Дата':
                    self.XY["time"]=y
                elif  self.df.iloc[x,y]=='Направление':
                    self.XY["direction"]=y
                elif self.df.iloc[x,y]=='Детектор':
                    self.XY["detector"]=y
                elif self.df.iloc[x,y]=='Данни от детектори [брой]':
                    self.XY["value"]=y
                    self.XY["row"]=x+1
                    return;

    def GetTime(self,row):
        time = ''
        mystr = self.df.iloc[row,self.XY["time"]]
        if mystr[2] == '.' and mystr[5] == '.'and mystr[10] == ' ' and mystr[13] == ':'and mystr[13] == ':'and  mystr[16] == ':':
            time = datetime.strptime(mystr,"%d.%m.%Y %H:%M:%S")
        return time

    def GetTimeInterval(self):
        self.values = []
        self.Time = self.GetTime(self.XY["row"])
        while self.Time == self.GetTime(self.XY["row"]):
            self.GetValue()
            self.XY['row'] +=1
            if self.XY['row'] >= self.rows-1:
                return False;
        return True;

    def cleanValues(self):
        self.Time = ''
        self.values = []

    def GetValue(self):
        det = self.df.iloc[self.XY["row"],self.XY["detector"]]
        val = self.df.iloc[self.XY["row"],self.XY["value"]]
        direct = self.df.iloc[self.XY["row"],self.XY["direction"]].replace("H","")
        if type(det) == int:        
            self.values.append({'direction':direct,
                                'value':int(val),
                                'detector':det})






