import sys
import TrafficDemand as TD
import header

#cfgfile,interval,routingAlgorithm,minGap,accel,decel,emergencyDecel,sigma,tau

td = TD.TrafficDemand()
for cfg in header.configFiles:
    for i in header.interval:
        for mg in header.minGap:
            for a in header.accel:
                for d in header.decel:
                    for e in header.emergencyDecel:
                        for s in header.sigma:
                            for t in header.tau:
                                for ra in header.routingAlgorithm:
                                    td.CalculateKrauss(cfg,str(i),ra,mg,a,d,e,s,t)
