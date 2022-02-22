import TrafficDemand as TD
import paths
interval = [10,20,30,40]
configFiles = ["wcfg.csv","hcfg.csv"]

'''
for cfg in configFiles:
    for i in interval:
        TD.CallFLowRouter(i,cfg)
        TD.CalculateKraussOrig1(paths.out_path,i)
        TD.CalculatePWagner2009(paths.out_path,i)
        TD.CalculateWiedemann(paths.out_path,i)
'''
TD.CallFLowRouter(30,"wcfg.csv")
TD.CalculateKraussOrig1(paths.out_path,30)
    #CalculatePWagner2009(data_path,interval[x])
    #CalculateWiedemann(data_path,interval[x])
