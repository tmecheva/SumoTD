import sys
import TrafficDemand as TD
import header
           
td = TD.TrafficDemand()
for cfg in header.configFiles:
    for i in header.interval:
        for gap in header.minGap:
            for t in header.tau:
                for alg in header.routingAlgorithm:
                    td.CalculatePWagner2009(cfg,i,alg,gap,t)
