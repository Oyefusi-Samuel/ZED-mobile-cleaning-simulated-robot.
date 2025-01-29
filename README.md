# ZED-mobile-cleaning-simulated-robot IGN GAZEBO.
![image](https://github.com/user-attachments/assets/05693079-0374-4f11-943a-48d90b5548c9)

Fisrt step in building the differential-drive ZED mobile cleaning robot:

Create your ros2 workspace (You can use any name for your workspace, but follow naming rules.)
```
mkdir ros_ws 
```
```
cd ros_ws
```
Create your src folder

```
mkdir src
```

In the src directory of your workspace clone the repo in it to work with robot pkg.
```
cd src
```

```
  git clone https://github.com/Oyefusi-Samuel/ZED-mobile-cleaning-simulated-robot..git
```
If you build the workspace and you see some errors pop up .You should upgrade pytest to a version that is 6.2 or higher. Use the following command
```
  pip install --upgrade pytest
```
Then build the workspace again:
```
  colcon build
```
**Source the workspace**
```
source install/setup.bash
```

**STEPS TO TAKE TO GET THE ROBOT UP AND READY:**
1. Lauch the robot in an empty world  

2. Visualize in Rviz .
   
3. check the TF2 TREE

Launch the Node:   (To visualize the robot in an empty gazebo world)
```
 ros2 launch robot show.robot.launch.py use_sim_time:=true
```
![Screenshot from 2024-12-19 13-42-21](https://github.com/user-attachments/assets/a2b43c19-0088-4ea7-a876-66cb8e40df39)

Launch the rviz Node:   (To visualize the robot joint, tf)
```
  ros2 launch robot display.launch.py 
```
![Screenshot from 2024-12-19 13-58-04](https://github.com/user-attachments/assets/76c54e3a-6fae-48f9-943f-bee063887dfe)

You can check the TF2 TREE:
```
  ros2 run rqt_tf_tree rqt_tf_tree
```
![Screenshot from 2024-12-19 14-40-35](https://github.com/user-attachments/assets/11522d88-2ae8-4230-a877-e5301900e78e)

**The centre of the robot is the "base_link".**

# Plugins used in simulation of the robot can be gotten from:
https://classic.gazebosim.org/tutorials?tut=ros_gzplugins

![image](https://github.com/user-attachments/assets/051a698d-09ee-4850-af7f-0cbf6805c6f0)

# Spawning the robot into a custom gazebo world:
To spawn the robot into gazebo, launch the file called show.robot.launch.py, ensure you save the custom designed gazebo world into the world directory in the src folder (Note: launch files in ROS 2 are python scripts/files)


# To LAUNCH THE WORLD:
 
```
   ros2 launch robot show.robot.launch.py world:="path to the .world file"
```
Mine is:
```
ros2 launch robot show.robot.launch.py world:='/home/sam/zed_robot/src/robot/worlds/cafeworld' 
```
![Screenshot from 2024-12-19 14-09-51](https://github.com/user-attachments/assets/c2dca134-85bb-4497-a191-8be6e65ca0ef)
![Screenshot from 2024-12-19 14-24-43](https://github.com/user-attachments/assets/08396e2a-4be4-48c1-9304-a7ec9c649b3d)

```
ros2 launch robot show.robot.launch.py world:='/home/sam/zed_robot/src/robot/worlds/outside.world' 
```
![Screenshot from 2024-12-19 14-36-34](https://github.com/user-attachments/assets/7292b490-bbdb-45b0-a8c8-3f22dfdf448f)

 Check if the topics are available.This list all **topics** which are available:
 ```
   ros2 topic list
 ```
 Now,we can drive the robot around once we use the teleop_twist_keyboard node to publish to the **"/cmd_vel" topic** that the robot subscribes to.
 
 ```
   ros2 run teleop_twist_keyboard  teleop_twist_keyboard
 ```
 
 You can give colour to the robot,by adding colour to the robot description .xacro file.

![image](https://github.com/user-attachments/assets/7a46493f-694c-4e51-80fe-e2468c98deed)

 

# SLAM 
Run the slam_toolbox node.
```
  ros2 launch ros2_mapping online_async_launch.py
```
Open rviz to visualize SLAM (add laserscan, mapp tf, robotmodel) topics 
```
rviz2
```
![image](https://github.com/user-attachments/assets/843966c5-dacb-4f51-88c3-ab611036c3e2)

 Now,we can drive the robot around using the teleop_twist_keyboard node to map the world.
 
 ```
   ros2 run teleop_twist_keyboard  teleop_twist_keyboard
 ```
![image](https://github.com/user-attachments/assets/2891d086-eb1c-4a34-9e52-9de18245f97c)

Save your map using the ros2 map server node 
```
ros2 run nav2_map_server map_saver_cli -f /path/to/save/map_name  # Saves the current map to the specified path and file name
```
mine was 
```
ros2 run nav2_map_server map_saver_cli -f /home/sam/zed_robot/src/ros2_mapping/map/map_2  # Saves the current map to the specified path and file name
```
![image](https://github.com/user-attachments/assets/b07b7de9-4e69-4792-8689-4c5317406154)

[ff.webm](https://github.com/user-attachments/assets/54a1b92b-fc27-4f83-9a48-a7cb5b1256fe)

# AMCL
Run the AMCL node.
```
 ros2 launch ros2_mapping amcl.launch.py
```
Open rviz to visualize SLAM (add Particlecloud, laserscan, mapp tf, robotmodel) topics, 2d pose estimate, you should see the particle cloud. 
```
rviz2
```

![image](https://github.com/user-attachments/assets/e5111874-074a-4082-a5dd-40fdc99b5ccb)

 Now,we can drive the robot around using the teleop_twist_keyboard node to visualize the particle cloud around. 
 
 ```
   ros2 run teleop_twist_keyboard  teleop_twist_keyboard
 ```

# AUTONOMOUS NAVIGATION:
 Localization:
 ```
ros2 launch ros2_mapping localization.launch.py
```

Navigation Mode(NAV2 stack)
```
 ros2 launch ros2_mapping navigation.py    # set 2d pose estimate of the robot to begin navigation
```

# INTERACT PROGRAMATICALLY WITH THE NAVIGATION STACK (python API)
   
   We can also write a python script that publish certain velocity to make the robot move and also perform some basic task. its dependecies on rclpy,the package should be created in the src directory of your workspace.
```
cd src
```
```
ros2 pkg create <name of pkg> --build-type ament_python --dependencies rclpy       # mine was ros2 pkg create drive_robot --build-type ament_python --dependencies rclpy

```

Install transformations packages 

```
sudo apt install ros-humble-tf-transformations
```
```
sudo apt install python3-transforms3d 
```

 Run the script in the pasckage to make the robot drive to goal 3.5,0  set in the code.
 
![Image](https://github.com/user-attachments/assets/ac2c774e-f86a-445b-be6f-b23cd3ececde)

![Image](https://github.com/user-attachments/assets/a6c909a8-4446-4182-b89a-77c06aaa6370)


# Converting Gazebo classic to Gazebo Ignition(Lastest Gazebo simulator)
Install required dependecies
```
  sudo apt install ros-<ros2_distro>-ros-ign-gazebo
  sudo apt install ros-humble-ros-ign-gazebo  # my current ros distro is humble, you can change to fit your ros version (foxy, jazzy)
  sudo apt install ros-humble-ros-gz-bridge
  sudo apt install ros-humble-ign-ros2-control
  sudo apt install ros-humble-twist-mux
  sudo apt install ros-humble-twist-stamper
  sudo apt install ros-humble-ros2-control
  sudo apt install ros-humble-ros2-controllers
```
## for example:
If you are using ros 2 humble distro , just replace <ros2_distro> with humble . So it will be :
```
  sudo apt install ros-humble-ros-gz
```





