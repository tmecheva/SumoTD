import sys
import TrafficDemand as TD
import paths

#configFiles = ["wcfg.csv","hcfg.csv"]
#interval = [10,20,30,40]
#routingAlgorithm = ['dijkstra','astar','CH']

#minGap = [1,1.5,2,2.5,3]
#tau = [1,1.25]#[0.25,0.5,0.75,0.9,1,1.25]


#command line arguments
#cfgfile interval routingAlgorithm minGap tau

td = TD.TrafficDemand()
row = td.CalculateKraussOrig(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
