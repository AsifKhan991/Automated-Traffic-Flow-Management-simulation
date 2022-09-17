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
    
    prevstep=3  
    step = 0
    x=0#edge number
    y=0#lane number
    ax=0
    ay=0
    while traci.simulation.getMinExpectedNumber() > 0:
        
        
        traci.simulation.step()
        
        i=0
        j=0
        
        n=[[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
        
        tls=[["G", "r", "r"],
             ["G", "r", "r"],
             ["G", "r", "r"],
             ["G", "r", "r"]]
        
        for i in range(4):
            for j in range(3):
                n[i][j]=traci.lane.getLastStepHaltingNumber("gneE"+str(i)+"_"+str(j))   #data entry loop
                
      
        
        s=0       
        at=0
        state=""
        
        for i in range(4):
            for j in range(1,3):
                if n[i][j]>s:        #comparing loop
                    s=n[i][j]
                    x=i
                    y=j
        if(2>1):
            
            tls[x][y]="G"
            
            if(y==1):
                az=(x+2)%4
                at=(x+1)%4
                if(n[x][2]>n[at][2]):
                    ax=x
                    ay=2
                elif(n[az][1]>n[at][2]):
                    ax=az
                    ay=1
                else:
                    ax=at
                    ay=2

            if(y==2):
                az=(x+3)%4
                at=(x+1)%4
                if(n[x][1]>n[az][1]):
                    ax=x
                    ay=1
                elif(n[at][2]>n[az][1]):
                    ax=at
                    ay=2
                else:
                    ax=az
                    ay=1
                    
        
                    
            tls[ax][ay]="G"
                          
        
            for i in range(4):
                for j in range(3):
                    if(i+1<=3):
                        state=state+tls[i+1][j]
                    else:
                        state=state+tls[0][j]
                
            ID="gneJ0"        
            traci.trafficlight.setRedYellowGreenState(ID,state)
            
            prevstep=step
            px=x
            py=y
            pax=ax
            pay=ay
            
        
        print(traci.vehicle.getIDCount());                   
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
