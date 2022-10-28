import sys
import TrafficDemand as TD
import header
#def CalculateWiedemann(self,cfgfile,interval,routingAlgorithm,minGap,security,estimation,tau):        

td = TD.TrafficDemand()
for cfg in header.configFiles:
    for i in header.interval:
        for alg in header.routingAlgorithm:
            for gap in header.minGap:
                for s in header.security:
                    for e in header.estimation:
                        for t in header.tau:
                            td.CalculateWiedemann(cfg,i,alg,gap,s,e,t)
