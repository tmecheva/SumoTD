import OutputFlows as OF

Ofl = OF.OutputFlows("/home/tedy/Sumo/2022-01-19-17-10-39/out.xml","/home/tedy/Sumo/Data/Config/wcfg.csv","/home/tedy/Sumo/Data/Config/inFlows.csv","/home/tedy/Sumo/Data/Results/cmp.csv")
Ofl.Compare()
#Ofl.STDEV()
#Ofl.STDEVdirection("/home/tedy/Sumo/ControllerReports/Out/cmp.csv")
