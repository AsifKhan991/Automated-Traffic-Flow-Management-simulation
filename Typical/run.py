#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args() 
    return options


# contains TraCI control loop
def run():

    
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        s=[]
        traci.simulation.step()
        i=0
        j=0
        n= [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],]
        
        for i in range(3):
            for j in range(2):
                n[i][j]=traci.lane.getLastStepOccupancy("gneE"+str(i)+"_"+str(j))
                j=j+1
            i=i+1
        s=traci.lane.getLastStepVehicleIDs("gneE1_0")
        for x in s:
            if "VIP" in x:
                print("yes")

            
        
            
        
        step += 1            
        
    traci.close()
    sys.stdout.flush()    

            
        

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "notls.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
