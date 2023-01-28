import header
import subprocess
import os

def CallFLowRouter(i,cfgfile):
    if not os.path.exists(os.path.join(header.config_path,i)):
        os.makedirs(os.path.join(header.config_path,i))
            
    cmd = 'python3 {script_path} -n {net_path} -d {detectors_path} -f {conf_path} -o {output_path} -e {flows_path} --params {prm}'.format(
        script_path=os.path.join(header.sumo_tools_path,"detector/flowrouter.py"),
        net_path=header.network_path,
        detectors_path=os.path.join(header.config_path,"detectors.xml"),
        conf_path=os.path.join(header.config_path,cfgfile+".csv"),
        output_path=os.path.join(header.config_path,i,"route.xml"),
        flows_path=os.path.join(header.config_path,i,"flow.xml"),
        interval=i,
        prm='\'type=\"type1\"\''
    )
    
    subprocess.run(cmd, shell=True)


for interval in header.interval:
    for cfg in header.configFiles:
        CallFLowRouter(interval,cfg)
