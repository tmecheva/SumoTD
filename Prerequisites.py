import sys
import os
import paths
import subprocess
import xml.etree.ElementTree as ET

#configFiles = ["wcfg.csv","hcfg.csv"]
#interval = [10,20,30,40,50]
routingAlgorithm = ['dijkstra','astar','CH']

#wcfg 50

class Prerequisites:
    def __init__(self,cfgfile,interval):
        self.cfg=str(cfgfile)+'.csv'
        self.i=str(interval)
        self.cfgpath=os.path.join(paths.out_path,str(cfgfile))
        self.ipath=os.path.join(paths.out_path,str(cfgfile),str(interval))
        
        if not os.path.isdir(self.cfgpath):
            os.mkdir(self.cfgpath)

        if not os.path.isdir(self.ipath):
            os.mkdir(self.ipath)
    
    def CallFLowRouter(self):
        command = "python3 "+paths.sumo_tools_path+"detector/flowrouter.py -n "+paths.network_path+" -d "+paths.simulation_path+"/detectors.xml -f "+paths.config_path+self.cfg+" -o "+os.path.join(self.ipath,"route.xml")+" -e "+os.path.join(self.ipath,"flow.xml")+" -i "+self.i+" --lane-based -v -y 'type=\"vdist1\"'"            
        subprocess.run(command,shell=True)
        
    def CalculatePrerequisites(self):
        self.CallFLowRouter()
        
        
Prq = Prerequisites(sys.argv[1],sys.argv[2])
Prq.CalculatePrerequisites()
