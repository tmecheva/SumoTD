#Concatenates all Departure and Arrival curves and output the dataframe to a csv file
import pandas as pd
import xml.dom.minidom as dom
import os
import header
from os.path import exists
import xml.etree.ElementTree as ET

class TestSim:
    def __init__(self):
        self.result_folders=[]
        print("TestSim is here!")
        
    def scanDir(self):
        if os.path.isdir("/home/tedy/Sumo/script/SumoTD/Result/wCFG"):
            dirName = "/home/tedy/Sumo/script/SumoTD/Result/wCFG"
        elif os.path.isdir("/home/tedy/Sumo/script/SumoTD/Result/hCFG"):
            dirName = "/home/tedy/Sumo/script/SumoTD/Result/hCFG"
            
        subfolders = [f.path for f in os.scandir(dirName)]
        self.result_folders = list(subfolders)
                               
    def CheckExecution(self):
        for fld in self.result_folders:
            path = os.path.join(fld,"out.xml")
            folder = os.path.basename(fld)
            if os.path.isfile(path):
                tree = ET.parse(path)
                root=tree.getroot()
                if root:
                    last_veh = root[-1].get('end')
                    if int(last_veh.split('.')[0]) not in range(86340,864060):
                        print("ERROR! In configuration ",folder," last vehicle arrived at ",last_veh)
                else:
                    print("ERROR! In configuration ",folder," no vehicles generated!")
            else:
                print("Error! Out file in "+folder+" is missing!!")
                
        
ts = TestSim()
ts.scanDir()
ts.CheckExecution()
