from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Find the directories of the required ROS 2 packages
    ros2_mapping_pkg_share = FindPackageShare('ros2_mapping')
    nav2_bringup_launch_file = PathJoinSubstitution(
        [FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py']
    )

    # Path to the RViz configuration file
    rviz_config_file = PathJoinSubstitution(
        [ros2_mapping_pkg_share, 'config', 'rviz.rviz']
    )

    # Launch Configuration variables
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare Launch Arguments
    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=PathJoinSubstitution([ros2_mapping_pkg_share, 'map', 'simple_world.yaml']),
        description='Full path to the map yaml file to load'
    )

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([ros2_mapping_pkg_share, 'config', 'nav2_params.yaml']),
        description='Full path to the ROS 2 parameters file for all nodes'
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time (Gazebo clock) if set to true'
    )

    # Include the nav2_bringup launch file with passed arguments
    nav2_bringup_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_bringup_launch_file),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
        }.items()
    )

    # Add RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    # Return the complete LaunchDescription
    return LaunchDescription([
        declare_map_yaml_cmd,
        declare_params_file_cmd,
        declare_use_sim_time_cmd,
        nav2_bringup_launch_cmd,
        rviz_node,  # Add RViz node here
    ])
