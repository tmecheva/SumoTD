import sys
import TrafficDemand as TD
import paths
interval = [10,20,30,40]
configFiles = ["wcfg.csv","hcfg.csv"]

#wconfig interval routingAlg minGap tau

td = TD.TrafficDemand()
td.CalculatePWagner2009(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
