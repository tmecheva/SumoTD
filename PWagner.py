import sys
import TrafficDemand as TD
import header
           
td = TD.TrafficDemand()
for cfg in header.configFiles:
    for i in header.interval:
        for alg in header.routingAlgorithm:
            for gap in header.minGap:
                for t in header.tau:
                    td.CalculatePWagner2009(cfg,i,alg,gap,t)
