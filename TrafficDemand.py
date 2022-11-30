import subprocess
import os
import pandas as pd
import header
import xml.etree.ElementTree as ET

#routeChoice = ['gawron','logit']
#routing-algorithm dijkstra, astar, CH, CHWrapper
'''
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
'''    
class TrafficDemand:
    def CallSumo(self,interval,algorithm,cfg):
        tree = ET.parse(os.path.join(header.simulation_path,"osm.sumocfg"))
        root = tree.getroot()
        for el in root:
            for subel in el:
                if subel.tag == 'route-files':
                    subel.set('value',os.path.join(header.out_path,cfg,'Dua.xml'))
                if subel.tag == 'additional-files':
                    subel.set('value',os.path.join(header.out_path,cfg,'detectors.xml'))
        tree.write(os.path.join(header.simulation_path,"osm.sumocfg"))
        
        command="sumo -c "+os.path.join(header.simulation_path,"osm.sumocfg")
        subprocess.run(command,shell=True)      
  
    def CreateFlowFile(self,line,path,interval,cfgfile):
        with open(os.path.join(header.out_path,cfgfile,interval,'flow.xml'), "r") as file:
            lines = file.readlines()
            if lines[1].find('carFollowModel'):
                lines[1]=line
            else:
                lines.insert(1,line)
        file.close()
        
        with open(os.path.join(path,'fl.xml'), 'w') as file:
            file.writelines(lines)
        file.close()
        
      
    def CreateAdditionalFile(self,path):
        tree = ET.parse(os.path.join(header.simulation_path,'detectors.xml'))
        root = tree.getroot()
        
        for el in root:
            el.attrib["file"] = os.path.join(path,'out.xml')

        tree.write(os.path.join(path,"detectors.xml"))
        
    def CallDuaRouter(self,cfg,cfgfile,interval,algorithm):            
        tree = ET.parse(os.path.join(header.config_path,'duaCFG.xml'))
        root = tree.getroot()
        for el in root:
            for subel in el:
                if subel.tag == 'net-file':
                    subel.set('value',header.network_path)
                if subel.tag == 'route-files':
                    subel.set('value',os.path.join(header.out_path,cfgfile,interval,"route.xml")+","+os.path.join(header.out_path,cfg,'fl.xml'))
                if subel.tag == 'output-file':
                    subel.set('value',os.path.join(header.out_path,cfg,'Dua.xml'))
                if subel.tag == 'routing-algorithm':
                    subel.set('value',algorithm)
        tree.write(os.path.join(header.out_path,cfg,'duaCFG.xml'))
        
        command='duarouter -c '+os.path.join(header.out_path,cfg,'duaCFG.xml')
        subprocess.run(command,shell=True)
        
    def CalculateKrauss(self,cfgfile,interval,routingAlgorithm,minGap,accel,decel,emergencyDecel,sigma,tau):
                
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Krauss"'+' minGap="'+str(minGap)+'" accel="'+str(accel)+'" decel="'+str(decel)+'" emergencyDecel="'+str(emergencyDecel)+str(decel)+'" sigma="'+str(sigma)+'" tau="'+str(tau)+'" />'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'K'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)+'a'+str(accel)+'d'+str(decel)+'e'+str(emergencyDecel)+str(decel)+'s'+str(sigma)
        cfg = cfg.replace('.','')
        
        path = os.path.join(header.result_path,cfgfile,cfg)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.CreateAdditionalFile(path)                    
        self.CreateFlowFile(line,path,interval,cfgfile)
        self.CallDuaRouter(path,cfgfile,interval,routingAlgorithm)
        self.CallSumo(interval,routingAlgorithm,path)                
                            
    def CalculateKraussOrig(self,cfgfile,interval,routingAlgorithm,minGap,tau):       
        
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="KraussOrig1"'+' minGap="'+str(minGap)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'KO'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        if not os.path.exists(os.path.join(header.result_path,cfgfile,cfg)):
            os.makedirs(os.path.join(header.result_path,cfgfile,cfg))
                    
        path = os.path.join(header.result_path,cfgfile,cfg)
        
        self.CreateAdditionalFile(path)        
        self.CreateFlowFile(line,path,interval,cfgfile)
        self.CallDuaRouter(path,cfgfile,interval,routingAlgorithm)
        self.CallSumo(interval,routingAlgorithm,path)                
                            
    def CalculatePWagner2009(self,cfgfile,interval,routingAlgorithm,minGap,tau):               
        line='<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="PWagner2009"'+' minGap="'+str(minGap)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'PW'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        if not os.path.exists(os.path.join(header.result_path,cfgfile,cfg)):
            os.makedirs(os.path.join(header.result_path,cfgfile,cfg))
            
        path = os.path.join(header.result_path,cfgfile,cfg)
        
        self.CreateAdditionalFile(path)        
        self.CreateFlowFile(line,path,interval,cfgfile)
        self.CallDuaRouter(path,cfgfile,interval,routingAlgorithm)
        self.CallSumo(interval,routingAlgorithm,path)             
           
    #interval routingAlgorithm minGap security estimation tau
    def CalculateWiedemann(self,cfgfile,interval,routingAlgorithm,minGap,security,estimation,tau):        
        line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Wiedemann"'+' minGap="'+str(minGap)+'" security="'+str(security)+'" estimation="'+str(estimation)+'" tau="'+str(tau)+'"/>'+'\n'
        
        cfg = str(cfgfile)+'i'+str(interval)+'W'+'a'+str(routingAlgorithm)+'g'+str(minGap)+'s'+str(security)+'e'+str(estimation)+'t'+str(tau)
        cfg = cfg.replace('.','')
        
        if not os.path.exists(os.path.join(header.result_path,cfgfile,cfg)):
            os.makedirs(os.path.join(header.result_path,cfgfile,cfg))
            
        path = os.path.join(header.result_path,cfgfile,cfg)
        
        self.CreateAdditionalFile(path)        
        self.CreateFlowFile(line,path,interval,cfgfile)
        self.CallDuaRouter(path,cfgfile,interval,routingAlgorithm)
        self.CallSumo(interval,routingAlgorithm,path)          


        
    


    

        
    
    
