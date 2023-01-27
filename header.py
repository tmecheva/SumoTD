import os

current_directory = os.getcwd()
simulation_path = os.path.join(current_directory,"simulation")
reports_path = os.path.join(current_directory,"Reports")
network_path=os.path.join(simulation_path,'DrivingHabits.net.xml')
sumo_tools_path = "/usr/share/sumo/tools/"
out_path= os.path.join(current_directory,'Out')
result_path= os.path.join(current_directory,'Result')
config_path = os.path.join(current_directory,"config")
vtype = " -y 'vtype=\"vdist1\"'"
junctions=['306','402','601','302','304','404','502']

routingAlgorithm = ['CH','dijkstra','astar']

configFiles = ["wCFG","hCFG"]
interval = [50]#['10','20','30','40','50']

minGap = [1]#,1.5,2,2.5,3]#5
accel = [2.5]#,2.6,2.7,2.8,2.9]#5
decel = [4]#,4.3,4.5,4.8,5]#5
emergencyDecel = [0]#,1,2,3]#4
sigma = [0]#,0.25,0.5,0.75,1]#5
tau = [0.25]#,0.5,0.75,0.9,1,1.25]#6 

security = [1]#,2,3,4,5,6]#6
estimation = [1]#,2,3,4,5,6]#6

cc1 = tau
cc2 = [1,2,3,4,5]
cc3 = [6,7,8,9,10,11,12]
cc4 = [-0.25,-0.5,-0.75,-1,-1.25,-1.5,-1.75,-2]
cc5 = [0.5,0.75,1,1.25,1.5,1.75,1,2.25,2.5,2.75]
cc6 = [9,10,11,12,13]
cc7 = [0.22,0.24,0.26,0.28,0.3,0.32,0.34]
cc8 = [1,1.5,2,2.5,3,3.5]
cc9 = [1.1,1.5,1.9,2.3,2.5]

#Wiedermann interval * routingAlgorithm * minGap * security * estimation *tau= 5 * 3 * 5 * 6 * 6 * 6 = 16 200
#Wagner interval * routingAlgorithm * minGap * tau= 5 * 3 * 5 * 6 = 450
#KraussOrig interval * routingAlgorithm * minGap * tau= 5 * 3 * 5 * 6 = 450
#Krauss interval * routingAlgorithm * minGap * accel * decel * emergencyDecel * sigma * tau = 5 * 3 * 5 * 5 * 5 * 4 * 5 * 6 = 225 000
#total - 242100 * 2 = 484200
