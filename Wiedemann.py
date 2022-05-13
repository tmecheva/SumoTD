import sys
import TrafficDemand as TD
import paths

configFiles = ["wcfg.csv","hcfg.csv"]
interval = [10,20,30,40]
routingAlgorithm = ['dijkstra','astar','CH']

minGap = [1,1.5,2,2.5,3]
security = [1,2,3,4,5,6]
estimation = [1,2,3,4,5,6]
tau = [1,1.25]#[0.25,0.5,0.75,0.9,1,1.25]


#command line arguments
#cfgfile interval routingAlgorithm minGap security estimation tau

td = TD.TrafficDemand()
row = td.CalculateWiedemann(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
