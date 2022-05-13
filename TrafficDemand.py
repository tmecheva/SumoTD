import subprocess
import sys
import os
import shutil
import pandas as pd
import paths
import xml.etree.ElementTree as ET

#routeChoice = ['gawron','logit']
routingAlgorithm = ['dijkstra','astar','CH']

configFiles = ["wcfg.csv","hcfg.csv"]
interval = [10,20,30,40,50]

minGap = [1,1.5,2,2.5,3]
accel = [2.5,2.6,2.7,2.8,2.9]
decel = [4,4.3,4.5,4.8,5]
emergencyDecel = [0,1,2,3]
sigma = [0,0.25,0.5,0.75,1]
tau = [1,1.25]#[0.25,0.5,0.75,0.9,1,1.25]
interval = [10,20,30,40]


security = [1,2,3,4,5,6]
estimation = [1,2,3,4,5,6]

cc1 = tau
cc2 = [1,2,3,4,5]
cc3 = [6,7,8,9,10,11,12]
cc4 = [-0.25,-0.5,-0.75,-1,-1.25,-1.5,-1.75,-2]
cc5 = [0.5,0.75,1,1.25,1.5,1.75,1,2.25,2.5,2.75]
cc6 = [9,10,11,12,13]
cc7 = [0.22,0.24,0.26,0.28,0.3,0.32,0.34]
cc8 = [1,1.5,2,2.5,3,3.5]
cc9 = [1.1,1.5,1.9,2.3,2.5]
'''

CarFollowingModel = [{'name':'Krauss','params':[('minGap',minGap),('accel',accel),('decel',decel),('emergencyDecel',emergencyDecel),('sigma',sigma),('tau',tau)]}]
                     #{'name':'KraussOrig1','params':[('minGap',minGap),('tau',tau)]},
                     #{'name':'PWagner2009','params':[('minGap',minGap),('tau',tau)]},
                     #{'name':'Wiedemann','params':[('minGap',minGap),('tau',tau),('security',security),('estimation',estimation)]}]
                     #{'name':'W99','params':['minGap':minGap,'tau':tau,'cc1':cc1,'cc2':cc2,'cc3':cc3,'cc3':cc3,cc5,cc6,cc7,cc8,cc9]}]
                     
                     
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">

    <input>
        <net-file value="/home/tedy/Sumo/2022-01-19-17-10-39/updated.net.xml"/>
        <route-files value="/home/tedy/Sumo/2022-01-19-17-10-39/route.xml,/home/tedy/Sumo/2022-01-19-17-10-39/flow.xml"/>
    </input>

    <output>
        <output-file value="/home/tedy/Sumo/2022-01-19-17-10-39/duaOut.xml"/>
        <keep-vtype-distributions value="true"/>
        <vtype-output value="/home/tedy/Sumo/2022-01-19-17-10-39/vOut.xml"/>
    </output>
    
    <processing>
        <weight-period value="10"/>
    </processing>

    <report>
        <verbose value="true"/>
    </report>

</configuration>

--route-choice-method gawron, logit, or lohse
--routing-algorithm dijkstra, astar, CH, CHWrapper

'''    
class TrafficDemand:
    def CallSumo(self,interval,algorithm,cfg):
        tree = ET.parse(os.path.join(paths.simulation_path,"osm.sumocfg"))
        root = tree.getroot()
        for el in root:
            for subel in el:
                if subel.tag == 'route-files':
                    subel.set('value',os.path.join(paths.out_path,self.cfgfile,interval,algorithm,cfg+'Dua.xml'))
        tree.write(os.path.join(paths.simulation_path+"osm.sumocfg"))
        
        command="sumo -c "+paths.simulation_path+"osm.sumocfg"
        subprocess.run(command,shell=True)
    
    def CalculateResult(self,cfg):
        OutTree = ET.parse(paths.simulation_path+'out.xml')
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

        dfIn = pd.read_csv(os.path.join(paths.config_path,self.cfgfile+'.csv'),sep=";")
        res = pd.merge(dfOut,dfIn,on=["Detector","Time"],how="inner",validate="one_to_one").fillna(-1)
        Diff = pd.DataFrame({'Diff' : []})
        Diff=res['qPKWcalc']-res['qPKW']
        res['Pow']=Diff.pow(2)
        res.to_csv(os.path.join(paths.result_path,cfg+'.csv'),index=False)         
  
    def CreateFlowFile(self,line,cfg,interval):
        with open(os.path.join(paths.out_path,self.cfgfile,interval,'flow.xml'), "r") as file:
            lines = file.readlines()
            if lines[1].find('carFollowModel'):
                lines[1]=line
            else:
                lines.insert(1,line)
        file.close()
        
        with open(os.path.join(paths.out_path,self.cfgfile,interval,cfg+'fl.xml'), 'w') as file:
            file.writelines(lines)
        file.close()
        
    def CallDuaRouter(self,interval,algorithm,cfg):
        path = os.path.join(paths.out_path,self.cfgfile,interval,algorithm)
        if not os.path.isdir(path):
            os.mkdir(path)
            
        tree = ET.parse(os.path.join(paths.config_path+'duaCFG.xml'))
        root = tree.getroot()
        for el in root:
            for subel in el:
                if subel.tag == 'net-file':
                    subel.set('value',os.path.join(paths.simulation_path,"updated.net.xml"))
                if subel.tag == 'route-files':
                    subel.set('value',os.path.join(paths.out_path,self.cfgfile,interval,"route.xml")+","+os.path.join(paths.out_path,self.cfgfile,interval,cfg+'fl.xml'))
                if subel.tag == 'output-file':
                    subel.set('value',os.path.join(paths.out_path,self.cfgfile,interval,algorithm,cfg+'Dua.xml'))
                if subel.tag == 'routing-algorithm':
                    subel.set('value',algorithm)
        tree.write(os.path.join(path,'duaCFG.xml'))
        
        command='duarouter -c '+os.path.join(path,'duaCFG.xml')
        subprocess.run(command,shell=True)
        
    def CalculateKrauss(self,cfgfile,interval,routingAlgorithm,minGap,accel,decel,emergencyDecel,sigma,tau):
        self.cfgfile=cfgfile
        
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Krauss"'+' minGap="'+str(minGap)+'" accel="'+str(accel)+'" decel="'+str(decel)+'" emergencyDecel="'+str(emergencyDecel)+str(decel)+'" sigma="'+str(sigma)+'" tau="'+str(tau)+'" />'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'K'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)+'a'+str(accel)+'d'+str(decel)+'e'+str(emergencyDecel)+str(decel)+'s'+str(sigma)
        cfg = cfg.replace('.','')
        
        self.CreateFlowFile(line,cfg,interval)
        self.CallDuaRouter(interval,routingAlgorithm,cfg)
        self.CallSumo(interval,routingAlgorithm,cfg)                
        self.CalculateResult(cfg)
                            
    def CalculateKraussOrig(self,cfgfile,interval,routingAlgorithm,minGap,tau):
        self.cfgfile=cfgfile
        
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="KraussOrig1"'+' minGap="'+str(minGap)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'KO'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        self.CreateFlowFile(line,cfg,interval)
        self.CallDuaRouter(interval,routingAlgorithm,cfg)
        self.CallSumo(interval,routingAlgorithm,cfg)                
        self.CalculateResult(cfg)
                            
    def CalculatePWagner2009(self,cfgfile,interval,routingAlgorithm,minGap,tau):
        self.cfgfile=cfgfile
        
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        
        line='<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="PWagner2009"'+' minGap="'+str(minGap)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'PW'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        self.CreateFlowFile(line,cfg,interval)
        self.CallDuaRouter(interval,routingAlgorithm,cfg)
        self.CallSumo(interval,routingAlgorithm,cfg)                
        self.CalculateResult(cfg)
           
    #interval routingAlgorithm minGap security estimation tau
    def CalculateWiedemann(self,cfgfile,interval,routingAlgorithm,minGap,security,estimation,tau):
        self.cfgfile=cfgfile
        
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Wiedemann"'+' minGap="'+str(minGap)+'" security="'+str(security)+'" estimation="'+str(estimation)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'W'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'s'+str(security)+'e'+str(estimation)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        self.CreateFlowFile(line,cfg,interval)
        self.CallDuaRouter(interval,routingAlgorithm,cfg)
        self.CallSumo(interval,routingAlgorithm,cfg)                
        self.CalculateResult(cfg)
        


        
    


    

        
    
    
