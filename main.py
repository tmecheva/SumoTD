import TrafficDemand as TD
import paths
interval = [10,20,30,40]
configFiles = ["wcfg.csv","hcfg.csv"]



'''
for cfg in configFiles:
    td = TD.TrafficDemand(paths.config_path+cfg)
    for i in interval:
        td.CallFLowRouter(i)
        td.CalculateKraussOrig1(paths.out_path,i)
        td.CalculatePWagner2009(paths.out_path,i)
        td.CalculateWiedemann(paths.out_path,i)
'''
td = TD.TrafficDemand(paths.config_path+"wcfg.csv")
td.CallFLowRouter(50)
td.CalculateKraussOrig1(paths.out_path,50)

