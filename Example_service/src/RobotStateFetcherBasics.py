import json
import sys
import threading
import time
import logging
import argparse
import gc


import bosdyn.client
from bosdyn.client import util
from bosdyn.client import spot_cam
from bosdyn.mission.client import MissionClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.docking import DockingClient
from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client import ResponseError, RpcError, create_standard_sdk
from flask import jsonify

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

detector_interface = "initialized"

class RobotStateHelpers:
    def __init__(self, robot, logger=_LOGGER):
        self.robot = robot
        self.robot.time_sync.wait_for_sync()
        self.robot_client = self.robot.ensure_client(RobotStateClient.default_service_name)
        self.mission_client = self.robot.ensure_client(MissionClient.default_service_name)
        self.graph_nav_client = self.robot.ensure_client(GraphNavClient.default_service_name)
        self.docking_client = self.robot.ensure_client(DockingClient.default_service_name)
    

    def get_robot_state(self): 
        
        resp = ""
        # Fore reference to all robot states: https://protect-eu.mimecast.com/s/zEjnCp2mwcOK31qDUkIjVZ?domain=dev.bostondynamics.com
        robot_state = self.robot_client.get_robot_state()
        # For reference: https://protect-eu.mimecast.com/s/Oc-PCr9oZfnolP79IxDroj?domain=dev.bostondynamics.com
        power_state = robot_state.power_state
        #print(power_state)
           
        # For reference: https://protect-eu.mimecast.com/s/Oc-PCr9oZfnolP79IxDroj?domain=dev.bostondynamics.com
        battery_state = robot_state.battery_states
        #print(battery_state)

        return(str(battery_state))
    def get_docking_state(self):
        # For reference: https://protect-eu.mimecast.com/s/ICWECyXylh2k5qKnSK4Jgo?domain=dev.bostondynamics.com

        # For refernece: https://protect-eu.mimecast.com/s/908sCzXzPhw9oQELfN7ca7?domain=dev.bostondynamics.com
        docking_state = self.docking_client.get_docking_state()
        #print(docking_state)
        start = str(docking_state).find("dock_type")
        s = str(docking_state)[0:start]
        s = s.replace("\n"," ")

        return (str(docking_state))
    def get_mission_state(self):
        # For reference to all MissionServices: https://protect-eu.mimecast.com/s/daxtCA1lqSl2ALBYtq-BWz?domain=dev.bostondynamics.com
 
        # For reference: https://protect-eu.mimecast.com/s/Oc-PCr9oZfnolP79IxDroj?domain=dev.bostondynamics.com
        mission_state = self.mission_client.get_state()
        #print(mission_state)
        return(str(mission_state))
    def get_localization_state(self):
        # For reference: https://protect-eu.mimecast.com/s/LSlECB6moIRB5p0otOsJDH?domain=dev.bostondynamics.com

        localization_state = self.graph_nav_client.get_localization_state()
        #print(localization_state)

    
    def run(self):
        #print("Running example... ")
        self.get_robot_state()
        self.get_mission_state()
        self.get_docking_state()
        self.get_localization_state()
    




def main(argv):
    
    import argparse

    parser = argparse.ArgumentParser()
 
    bosdyn.client.util.add_base_arguments(parser)
 
    bosdyn.client.util.add_service_hosting_arguments(parser)

    options, _ = parser.parse_known_args(argv)
    bosdyn.client.util.setup_logging(verbose=options.verbose)
    self_ip = bosdyn.client.common.get_self_ip(options.hostname)
    # Create robot object.
    sdk = create_standard_sdk('RobotStateClient', [MissionClient])
    robot = sdk.create_robot(options.hostname)
    #spot_cam.register_all_service_clients(sdk)
    f= open('output.txt', 'a')
    f.write("\n")
    f.write(str(sdk.robots))
    f.write("\n")
    f.write(str(threading.activeCount()))
    f.close()
    robot.authenticate("budadmin", "Bostondynamicsadmin")
    robot.start_time_sync(time_sync_interval_sec=1)
    robot.time_sync.wait_for_sync()
    detector_interface = RobotStateHelpers(robot, logger=_LOGGER)
    resp = detector_interface.get_robot_state()
    resp2 = detector_interface.get_docking_state()
    resp3 = detector_interface.get_mission_state()
    #f= open('output.txt', 'a')
    #f.write("RobotStateFetcherReturning")
    #f.close()
    sdk.clear_robots()
    del detector_interface
    del sdk
    del robot
    gc.collect
    return(resp + "\n" + resp2 + "\n" + resp3)
    
    try:
        # Thread to constantly scan the ring camera
        detector_thread = threading.Thread(target=detector_interface.run, args=())
        detector_thread.start()
    except (ResponseError, RpcError) as err:
        _LOGGER.error("[Main] Failed to initialize robot communication: %s" % err)
        return False
    
if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)

