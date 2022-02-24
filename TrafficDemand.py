import subprocess
import sys
import os
import xml.etree.ElementTree as ET
import shutil
import pandas as pd
import OutputFlows as OF
import paths

#routeChoice = ['gawron','logit']
routingAlgorithm = ['dijkstra','astar','CH']

minGap = [1,1.5,2,2.5,3]
accel = [2.5,2.6,2.7,2.8,2.9]
decel = [4,4.3,4.5,4.8,5]
emergencyDecel = [0,1,2,3]
sigma = [0,0.25,0.5,0.75,1]
tau = [1,1.25]#[0.25,0.5,0.75,0.9,1,1.25]
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
    def __init__(self,cfgfile):
        self.cfgfile = cfgfile

    def CallFLowRouter(self,interval):
        i=str(interval)
        command = "python3 "+paths.sumo_tools_path+"detector/flowrouter.py -n "+paths.network_path+" -d "+paths.simulation_path+"/detectors.xml -f "+self.cfgfile   +" -o "+paths.out_path+"route"+i+".xml -e "+paths.out_path+"flow"+i+".xml -i "+i+" --lane-based -v -y 'type=\"vdist1\"'"            
        subprocess.run(command,shell=True)    

    def CallDuaRouter(self):
        command='duarouter -c '+paths.out_path+'duaCFG.xml'
        subprocess.run(command,shell=True)
    
    def CallSumo(self):
        command="sumo -c "+paths.simulation_path+"osm.sumocfg"
        subprocess.run(command,shell=True)
    
    def ConfigDua(self,interval,config):
        tree = ET.parse(paths.out_path+'duaCFG.xml')
        root = tree.getroot()
        df = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        for algorithm in routingAlgorithm:
            for el in root:
                for subel in el:
                    if subel.tag == 'routing-algorithm':
                        subel.set('value',algorithm)
            r = config.replace('<vType id="vdist1" vClass="passenger" color="1,0,0"','').replace('/>','') + 'interval="'+str(interval)+'/" alg=/"'+algorithm
            tree.write(paths.out_path+'duaCFG.xml')
            self.CallDuaRouter()
            self.CallSumo()
            df =df.append(self.CalculateResult(r),ignore_index=True)
        return df

    def CalculateResult(self,config):
        StatTree = ET.parse(paths.simulation_path+'stat.xml')
        root=StatTree.getroot()
        for child in root.iter():
            if child.tag == 'safety':
                collision=child.get('collisions')
        Ofl = OF.OutputFlows(self.cfgfile)
        error = Ofl.Compare()
        row={'Config':config,'Error':error,'Collision':collision}
        return row      
    
    def CreateFlowFile(self,i,line):
        flowfile=paths.out_path+'flow'+str(i)+'.xml'
        ff = open(flowfile)
        nf = open(paths.out_path+'flow.xml', 'a')
        shutil.copyfile(paths.out_path+'route'+str(i)+'.xml',paths.out_path+'route.xml')
        doIHaveToCopyTheLine=False
        for l in ff.readlines():
            nf.write(l)
            if '<additional>' in l:
                doIHaveToCopyTheLine=True
            if doIHaveToCopyTheLine:
                nf.write(line)
                doIHaveToCopyTheLine=False                                
        ff.close()
        nf.close()
        df = self.ConfigDua(i,line)
        os.remove(paths.out_path+'flow.xml')
        os.remove(paths.out_path+'route.xml')
        return df
    
    def CalculateKrauss(self,ofile,i):
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        for m in range(0,len(minGap)):
            for a in range(0,len(accel)):
                for d in range(0,len(decel)):
                    for e in range(0,len(emergencyDecel)):
                        for s in range(0,len(sigma)):
                            for t in range(0,len(tau)):
                                line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Krauss"'+' minGap="'+str(minGap[m])+'" accel="'+str(accel[a])+'" decel="'+str(decel[d])+'" emergencyDecel="'+str(emergencyDecel[e]+decel[d])+'" sigma="'+str(sigma[s])+'" tau="'+str(tau[t])+'" />'+'\n'
                                df = self.CreateFlowFile(i,line)
                                result.append(df,ignore_index=True)
        result.to_csv(ofile)
                            
    def CalculateKraussOrig1(self,opath,i):
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        for m in minGap:
            for t in tau:
                line='\t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="KraussOrig1"'+' minGap="'+str(m)+'" tau="'+str(t)+'"/>'+'\n'
                df = self.CreateFlowFile(i,line)
                result = result.append(df,ignore_index=True)
        ofile = opath+"KraussOrig1/"+str(i)+".csv"
        result.to_csv(ofile)
                            
    def CalculatePWagner2009(self,ofile,i):
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        for m in range(0,len(minGap)):
            for t in range(0,len(tau)):
                line='<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="PWagner2009"'+' minGap="'+str(minGap[m])+'" tau="'+str(tau[t])+'"/>'+'\n'
                df = self.CreateFlowFile(i,line)
                result.append(df,ignore_index=True)
        result.to_csv(ofile)
                            
    def CalculateWiedemann(self,ofile,i):
        result = pd.DataFrame(columns = ['Config', 'Error', 'Collision'])
        for m in range(0,len(minGap)):
            for s in range(0,len(security)):
                for e in range(0,len(estimation)):
                    for t in range(0,len(tau)):
                        line='/t<vType id="vdist1" vClass="passenger" color="1,0,0" carFollowModel="Wiedemann"'+' minGap="'+str(minGap[m])+'" security="'+str(security[s])+'" estimation="'+str(estimation[e])+'" tau="'+str(tau[t])+'"/>'+'\n'
                        df = self.CreateFlowFile(i,line)
                        result.append(df,ignore_index=True)
        result.to_csv(ofile)
        


        
    


    

        
    
    
