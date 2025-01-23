import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
  DeclareLaunchArgument,
  ExecuteProcess,
  IncludeLaunchDescription,
  RegisterEventHandler,
  SetEnvironmentVariable)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit
 
def generate_launch_description():
  # Set the path to this package.
  my_pkg_path = get_package_share_directory('robot')

  # robot name
  robot_name = 'zed_bot'
  # initial robot pose
  x_pos = 0.0; y_pos = 0.0; z_pos = 0.0; yaw = 0.0

  # Set the path to the world file
  world_file_name = 'empty.sdf'
  world_file_path = os.path.join(my_pkg_path, 'worlds', world_file_name)

  # Set rviz config file
  rviz_file_name = 'robot_sim.rviz'
  rviz_file_path = os.path.join(my_pkg_path, 'config', rviz_file_name)
 

  # set some ignition environment variable
  gz_models_path = os.path.join(my_pkg_path, "models")
  gz_sim_system_plugin_path = '/opt/ros/humble/lib/'

  set_env_ign_resource_cmd = SetEnvironmentVariable(
          name="IGN_GAZEBO_RESOURCE_PATH",
          value=gz_models_path,
      )
  set_env_ign_model_cmd = SetEnvironmentVariable(
          name="IGN_GAZEBO_MODEL_PATH",
          value=gz_models_path,
      )
  
  set_env_ign_path_cmd = SetEnvironmentVariable(
          name="GZ_SIM_SYSTEM_PLUGIN_PATH",
          value=gz_sim_system_plugin_path,
      )
  #---------------------------------------------------
 

  # Launch configuration variables specific to simulation
  headless = LaunchConfiguration('headless')
  use_sim_time = LaunchConfiguration('use_sim_time')
  world_path = LaunchConfiguration('world_path')
  rviz_path = LaunchConfiguration('rviz_path')
  use_rviz = LaunchConfiguration('use_rviz')
  gz_verbosity = LaunchConfiguration('gz_verbosity')
  use_ekf = LaunchConfiguration('use_ekf')
  odom_topic = LaunchConfiguration('odom_topic')
 
  declare_headless_cmd = DeclareLaunchArgument(
    name='headless',
    default_value='False',
    description='Whether to run only gzserver')
     
  declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')
 
  declare_world_path_cmd = DeclareLaunchArgument(
    name='world_path',
    default_value=world_file_path,
    description='Full path to the world model file to load')
  
  declare_rviz_path_cmd = DeclareLaunchArgument(
    name='rviz_path',
    default_value=rviz_file_path,
    description='Full path to the world model file to load')
  
  declare_use_rviz_cmd = DeclareLaunchArgument(
    'use_rviz',
    default_value= 'True',
    description='whether to run sim with rviz or not')
  
  declare_gz_verbosity_cmd = DeclareLaunchArgument(
    'gz_verbosity',
    default_value= '3',
    description='Verbosity level for Ignition Gazebo (0~4).')
  
  declare_use_ekf_cmd = DeclareLaunchArgument(
      name='use_ekf',
      default_value='True',
      # default_value='False',
      description='fuse odometry and imu data if true')
  
  declare_odom_topic_cmd = DeclareLaunchArgument(
      name='odom_topic',
      default_value='odom',
      description='topic to remap /odometry/filtered to')
  #------------------------------------------------------------


  # Specify the actions
  rsp_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(my_pkg_path,'launch','rsp.launch.py')]
            ), 
            launch_arguments={'use_sim_time': use_sim_time}.items()
  )

  rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_path],
        output='screen',
        condition=IfCondition(use_rviz)
  )


  start_ign_gazebo = ExecuteProcess(
            condition=UnlessCondition(headless),
            cmd=['ign', 'gazebo',  '-r', '-v', gz_verbosity, world_path],
            output='screen',
            # shell=False,
        )
        
  
  start_ign_gazebo_headless = ExecuteProcess(
            condition=IfCondition(headless),
            cmd=['ign', 'gazebo',  '-r', '-v', gz_verbosity, '-s', '--headless-rendering', world_path],
            output='screen',
            # shell=False,
        )
        

  bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan",
            "/imu/data@sensor_msgs/msg/Imu[ignition.msgs.IMU",
            # "/sky_cam@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/camera@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo",
            # Clock message is necessary for the diff_drive_controller to accept commands https://github.com/ros-controls/gz_ros2_control/issues/106
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
        ],
        output="screen",
    )
  
  spawn_entity_in_ign = Node(
      package='ros_gz_sim',
      executable='create',
      output='screen',
      arguments=[
          '-topic', 'robot_description', 
          '-name', robot_name,
          '-allow_renaming', 'true',
          '-x', str(x_pos),
          '-y', str(y_pos),
          '-z', str(z_pos),
          '-Y', str(yaw),
          ],
      parameters=[{"use_sim_time": use_sim_time}]
      )

  load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        # shell=False,
        output="screen",
    )

  load_diff_drive_base_controller = ExecuteProcess(
      cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'diff_drive_base_controller'],
      # shell=False,
      output="screen",
  )
    
  start_joint_state_controller_after_spawning_entity = RegisterEventHandler(
                                      event_handler=OnProcessExit(
                                          target_action=spawn_entity_in_ign,
                                          on_exit=[load_joint_state_broadcaster],
                                      )
                                  )
  start_diff_drive_base_control_after_joint_state_Controller = RegisterEventHandler(
                                      event_handler=OnProcessExit(
                                          target_action=load_joint_state_broadcaster,
                                          on_exit=[load_diff_drive_base_controller],
                                      )
                                  )

  relay_odom = Node(
        name="relay_odom",
        package="topic_tools",
        executable="relay",
        parameters=[
            {
                "input_topic": "/diff_drive_base_controller/odom",
                "output_topic": "/wheel/odometry",
            }
        ],
        output="screen",
    )

  relay_cmd_vel = Node(
        name="relay_cmd_vel",
        package="topic_tools",
        executable="relay",
        parameters=[
            {
                "input_topic": "/cmd_vel",
                "output_topic": "/diff_drive_base_controller/cmd_vel_unstamped",
            }
        ],
        output="screen",
    )
  
  # Localize using odometry and IMU data. 
  # It can be turned off because the navigation stack uses AMCL with lidar data for localization
  ekf_config_path = os.path.join(my_pkg_path,'config','ekf.yaml')
  ekf_node = Node(
          package='robot_localization',
          executable='ekf_node',
          name='ekf_filter_node',
          output='screen',
          parameters=[
              ekf_config_path,
              {"use_sim_time": use_sim_time},
          ],
          condition=IfCondition(use_ekf),
          remappings=[("odometry/filtered", odom_topic)]
      )
  
  # Create the launch description
  ld = LaunchDescription()

  ld.add_action(set_env_ign_resource_cmd)
  ld.add_action(set_env_ign_model_cmd)
  ld.add_action(set_env_ign_path_cmd)
 
  # add the necessary declared launch arguments to the launch description
  ld.add_action(declare_headless_cmd)
  ld.add_action(declare_use_sim_time_cmd)
  ld.add_action(declare_world_path_cmd)
  ld.add_action(declare_rviz_path_cmd)
  ld.add_action(declare_use_rviz_cmd)
  ld.add_action(declare_gz_verbosity_cmd)
  ld.add_action(declare_use_ekf_cmd)
  ld.add_action(declare_odom_topic_cmd)
 
  # Add the nodes to the launch description
  ld.add_action(rsp_launch)
  ld.add_action(rviz_node)
  ld.add_action(start_ign_gazebo)
  ld.add_action(start_ign_gazebo_headless)
  ld.add_action(bridge)
  ld.add_action(spawn_entity_in_ign)
  ld.add_action(start_joint_state_controller_after_spawning_entity)
  ld.add_action(start_diff_drive_base_control_after_joint_state_Controller)
  ld.add_action(relay_odom)
  ld.add_action(relay_cmd_vel)
  ld.add_action(ekf_node)

 
  return ld