from launch import LaunchDescription
from launch_ros.actions import Node 

def launh_node():
    detected_cmd = Node(package ='propotional_bump_go',executable=' bump_go_node',parameters=[{'use_sim_time':True}])

    ld = LaunchDescription()
    ld.add_action(detected_cmd)
    return ld