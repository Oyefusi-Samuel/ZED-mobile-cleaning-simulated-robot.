# New gazebo sim launch file for the ros 2 simulated robot
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
# from launch.actions import ExecuteProcess


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='robot' # Variable name that saves the package name called robot.

    show = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','robot.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    
    # Adding default world 
    default_world = os.path.join(
        get_package_share_directory(package_name),
        'worlds',
        'new.world'  # Add the world here
    )
    
    world = LaunchConfiguration('world')
    
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='world to world'
    )
    
    
    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gazebo.launch.py')]), # changed package name from "gazebo_ros" to "ros_gz_sim"
                    launch_arguments= {'gz_args' : ['-r -v4 ', world], 'on_exit_shutdown': 'true'}.items() # add path_to_the_world_file
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create', # changed package name from "gazebo_ros" to "ros_gz_sim"
                        arguments=['-topic', 'robot_description',
                                   '-name', 'my_bot',
                                   '-z','0.1'],    
                        output='screen')
    
    # set_contoller_manager_use_sim_time = ExecuteProcess(
    #     cmd=['ros2', 'param', 'set', '/controller_manager', 'use_sim_time', 'true'],
    #     output='screen')


    # Launch them all!
    return LaunchDescription([ 
        DeclareLaunchArgument(
         'use_sim_time',
        default_value='false',
        description='Use sim time if true'), 
        show,
        gazebo,
        world_arg,
        spawn_entity,
        #set_contoller_manager_use_sim_time ,
    ])