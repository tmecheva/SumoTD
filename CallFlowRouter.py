import sys
import os
import subprocess
import header

def CallFLowRouter(cfgfile,i):
    
    cmd = 'python3 {script_path} -n {net_path} -d {detectors_path} -f {conf_path} -o {output_path} -e {flows_path} '.format(
        script_path=os.path.join(header.sumo_tools_path,"detector/flowrouter.py"),
        net_path=header.network_path,
        detectors_path=os.path.join(header.simulation_path+"/detectors.xml"),
        conf_path=os.path.join(header.config_path,cfgfile+".csv"),
        output_path=os.path.join(header.out_path,cfgfile,i,"route.xml"),
        flows_path=os.path.join(header.out_path,cfgfile,i,"flow.xml"),
        interval=i
    )
    
    subprocess.run(cmd, shell=True)

def CreateRouteFiles():
    for f in header.configFiles:
        if not os.path.exists(os.path.join(header.out_path,f)):
            os.makedirs(os.path.join(header.out_path,f))
        for interval in header.interval:
            if not os.path.exists(os.path.join(header.out_path,f,str(interval))):
                os.makedirs(os.path.join(header.out_path,f,str(interval)))
            CallFLowRouter(f,str(interval))
        
CreateRouteFiles()

