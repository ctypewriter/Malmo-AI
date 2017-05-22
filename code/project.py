""" Po of the poros has trouble making his way to his destination, but perhaps his descendants will do better."""


import MalmoPython
import os
import sys
import time
import poro

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately


endLocationx = 0
endLocationz = 10


# ModSettings affects simulation speed

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ModSettings>
                <MsPerTick> 20 </MsPerTick>
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
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>Poro</Name>
                <AgentStart>
                    <Placement x=".5" y="4" z="0"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  
                  <RewardForTouchingBlockType>
                  <Block reward="5000.0" type="diamond_block" behaviour="onceOnly"/>
                  </RewardForTouchingBlockType>
                  
                  
                  <RewardForTimeTaken 
                  initialReward="0"
                  delta="-1"
                  density="PER_TICK"
                  />
                  
                  <AgentQuitFromTouchingBlockType>
                    <Block type="diamond_block" />
                   </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


if __name__ == '__main__':
    # Create default Malmo objects:

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agent_host.getUsage()
        exit(1)
    if agent_host.receivedArgument("help"):
        print agent_host.getUsage()
        exit(0)


    # Runs AI however many times
    for i in range(5): # TODO change number of times to number of generations * population/generation
        my_mission = MalmoPython.MissionSpec(missionXML, True)
        # my_mission.forceWorldReset()
        my_mission.drawBlock(endLocationx,3,endLocationz,"diamond_block") # Draws the target location
        my_mission_record = MalmoPython.MissionRecordSpec()


        po = poro.Poro() # AI instant creator, TODO: Pass in value of attributes.

        # Attempt to start a mission:
        max_retries = 3
        for retry in range(max_retries):
            try:
                agent_host.startMission( my_mission, my_mission_record )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:",e
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        print "Waiting for the mission to start ",
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()


        print
        print "Mission running ",
        # Loop until mission ends:

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()

            print "reward: ", world_state.rewards[0].getValue()

            po.run(agent_host)




            for error in world_state.errors:
                print "Error:",error.text


        # returns reward result from the AI
        # for reward in world_state.rewards:
        #     print reward.getValue()

        print
        print "Mission ended"
        # Mission has ended.
