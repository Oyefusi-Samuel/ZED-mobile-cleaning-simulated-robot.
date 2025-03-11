import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
    # delare any path variable
    description_pkg_path = get_package_share_directory('zed_bot_description')
    base_pkg_path = get_package_share_directory('zed_bot_base')

    # Launch configuration variables specific to simulation
    use_ekf = LaunchConfiguration('use_ekf')
    odom_topic = LaunchConfiguration('odom_topic')

    declare_use_ekf_cmd = DeclareLaunchArgument(
      name='use_ekf',
      default_value='False',
      description='fuse odometry and imu data if true')

    declare_odom_topic_cmd = DeclareLaunchArgument(
      name='odom_topic',
      default_value='odom',
      description='topic to remap /odometry/filtered to')
    
    # create needed nodes or launch files
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(description_pkg_path,'launch','rsp.launch.py')]), 
        launch_arguments={'use_sim_time': 'False',
                          'use_joint_state_pub': 'False'}.items())
    

    robot_controllers = os.path.join(base_pkg_path,'config','epmc_diff_drive_controller.yaml')

    # see -> https://github.com/ros-controls/ros2_control_demos/blob/humble/example_2/bringup/launch/diffbot.launch.py
    # see -> https://control.ros.org/master/doc/ros2_control/controller_manager/doc/userdoc.html
    controller_manager_with_ekf = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        output="both",
        condition=IfCondition(use_ekf),
        remappings=[
            ("~/robot_description", "/robot_description"),
            ("/epmc_diff_drive_controller/cmd_vel_unstamped", "/cmd_vel"),
            ("/epmc_diff_drive_controller/odom", "/wheel/odometry"),
        ],
    )

    controller_manager_without_ekf = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        output="both",
        condition=UnlessCondition(use_ekf),
        remappings=[
            ("~/robot_description", "/robot_description"),
            ("/epmc_diff_drive_controller/cmd_vel_unstamped", "/cmd_vel"),
            ("/epmc_diff_drive_controller/odom", odom_topic),
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    epmc_diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["epmc_diff_drive_controller"],
    )    

    # Delay start of robot_controller after `joint_state_broadcaster`
    start_epmc_diff_drive_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[epmc_diff_drive_controller_spawner],
        )
    )


    eimu_ros_config_file = os.path.join(base_pkg_path,'config','eimu_ros_start_params.yaml')
    eimu_ros_node = Node(
        package='eimu_ros',
        executable='eimu_ros',
        name='eimu_ros',
        output='screen',
        parameters=[
            eimu_ros_config_file
        ],
        condition=IfCondition(use_ekf)
    )

    ekf_config_path = os.path.join(base_pkg_path,'config','ekf.yaml')
    ekf_node = Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                ekf_config_path
            ],
            condition=IfCondition(use_ekf),
            remappings=[("odometry/filtered", odom_topic)]

        )

    # Create the launch description and populate
    ld = LaunchDescription()

    # add the necessary declared launch arguments to the launch description
    ld.add_action(declare_use_ekf_cmd)
    ld.add_action(declare_odom_topic_cmd)
    

    # Add the nodes to the launch description
    ld.add_action(rsp_launch)
    ld.add_action(controller_manager_with_ekf)
    ld.add_action(controller_manager_without_ekf)
    ld.add_action(joint_state_broadcaster_spawner)
    ld.add_action(start_epmc_diff_drive_controller_spawner_after_joint_state_broadcaster_spawner)
    ld.add_action(eimu_ros_node)
    ld.add_action(ekf_node)

    return ld      # return (i.e send) the launch description for excecution