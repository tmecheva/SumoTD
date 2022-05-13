import sys
import TrafficDemand as TD
import paths
interval = [10,20,30,40]
configFiles = ["wcfg.csv","hcfg.csv"]

#wconfig interval minGap accel decel emergencyDecel sigma tau

td = TD.TrafficDemand()
td.CalculateKrauss(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9])
