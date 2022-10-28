import TrafficDemand as TD
import header

td = TD.TrafficDemand()
for cfg in header.configFiles:
    for i in header.interval:
        for algo in header.routingAlgorithm:
            for g in header.minGap:
                for t in header.tau:
                    td.CalculateKraussOrig(cfg,i,algo,g,t)
