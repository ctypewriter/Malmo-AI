""" Po of the poros has trouble making his way to his destination, but perhaps his descendants will do better."""

import MalmoPython
import os
import sys
import time
import poro

from math import floor

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

endLocationx = 1
endLocationy = 6
endLocationz = 14

# ModSettings affects simulation speed

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Poro is looking for the diamond!</Summary>
              </About>
              
              <ModSettings>
                <MsPerTick> 25 </MsPerTick>
              </ModSettings>
              
              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
                
                <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,3*3;1;village"/>
                  <DrawingDecorator>
                        <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>
                        <DrawCuboid x1="30" y1="4" z1="30" x2="30" y2="30" z2="-30" type="dirt"/>
                        <DrawCuboid x1="-30" y1="4" z1="30" x2="-30" y2="30" z2="-30" type="dirt"/>
                        <DrawCuboid x1="-30" y1="4" z1="-30" x2="30" y2="30" z2="-30" type="dirt"/>
                        <DrawCuboid x1="-30" y1="4" z1="30" x2="30" y2="30" z2="30" type="dirt"/>
                    </DrawingDecorator>
                  
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>Poro</Name>
                <AgentStart>
                    <Placement x=".5" y="4" z=".5"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <MissionQuitCommands/>
                  <RewardForTouchingBlockType>
                  <Block reward="5000.0" type="diamond_block" behaviour="onceOnly"/>
                  </RewardForTouchingBlockType>
                  <ObservationFromGrid>
                     <Grid name="floor-1">
                       <min x="-1" y="-1" z="-1"/>
                       <max x="1" y="-1" z="1"/>
                     </Grid>

                     <Grid name="floor0">
                       <min x="-1" y="0" z="-1"/>
                       <max x="1" y="0" z="1"/>
                     </Grid>

                     <Grid name="floor1">
                       <min x="-1" y="1" z="-1"/>
                       <max x="1" y="1" z="1"/>
                     </Grid>
                  </ObservationFromGrid>
                  
                  <AgentQuitFromTouchingBlockType>
                        <Block type="diamond_block"/>
                  </AgentQuitFromTouchingBlockType>
                  

                </AgentHandlers>
              </AgentSection>
            </Mission>'''

if __name__ == '__main__':



    # Create default Malmo objects:

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print 'ERROR:', e
        print agent_host.getUsage()
        exit(1)
    if agent_host.receivedArgument("help"):
        print agent_host.getUsage()
        exit(0)

    # .5 is the offset for center of the block
    po = poro.Poro(endLocationx + .5, endLocationy + .5 , endLocationz + .5)  # AI instantance creator

    # Runs AI however many times
    num_runs = 10000
    for i in range(num_runs):  # TODO change number of times to number of generations * population/generation
        my_mission = MalmoPython.MissionSpec(missionXML, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        # my_mission.forceWorldReset() # UNCOMMENT THIS WHEN CHANGING GEOGRAPHY

        my_mission.drawCuboid(endLocationx - 2, endLocationy - 2, endLocationz - 2, endLocationx +2, endLocationy -2,
                              endLocationz +2, "dirt")
        my_mission.drawCuboid(endLocationx - 1, endLocationy - 1, endLocationz - 1, endLocationx + 1, endLocationy -1,
                              endLocationz + 1, "dirt")
        my_mission.drawBlock(endLocationx, endLocationy, endLocationz, "diamond_block")  # Draws the target location


        #my_mission.drawBlock(endLocationx, endLocationy, endLocationz, "diamond_block")  # Draws the target location


        # Attempt to start a mission:
        max_retries = 3
        for retry in range(max_retries):
            try:
                agent_host.startMission(my_mission, my_mission_record)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:", e
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()


        world_state = agent_host.getWorldState()

        print i, ' ',
        po.run(agent_host)

        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:", error.text

        # returns reward result from the AI

        agent_host.sendCommand('quit')
        print
        print "Mission ended"
        # Mission has ended.
