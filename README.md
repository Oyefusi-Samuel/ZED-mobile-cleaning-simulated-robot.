# ZED-mobile-cleaning-simulated-robot.
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









</br></br></br></br></br></br></br></br></br></br></br></br></br>

## NEW README FOR ZED BOT

#### Prequisite
- Ensure you have already setup the motor's velocity PID with the **`Easy PID Motor Controller (EPMC) Module`** via the EPMC Setup Application GUI.

- Ensure you have already calibrated and set up the **`Easy IMU (EIMU) Module`** via the EIMU Setup Application GUI.

- In the `src/` folder of your `ros workspace`, clone the repo **epmc_hardware_interface** ROS2 plugin package
  (or you can download and add it manually to the `src/` folder)
  ```shell
  git clone https://github.com/robocre8/epmc_hardware_interface.git
  ```
  
- In the `src/` folder of your `ros workspace`, clone the repo **eimu_ros** ROS2 package
  (or you can download and add it manually to the `src/` folder)
  ```shell
  git clone https://github.com/robocre8/eimu_ros.git
  ```
  
- ensure you have the libserial package installed on your linux PC
  ```shell
    sudo apt install libserial-dev
  ```
  
- from the `src/` folder, cd into the root directory of your `ros workspace` and run rosdep to install all necessary ros dependencies for the **EPMC** and **EIMU** ros packages
  ```shell
  cd ../
  rosdep install --from-paths src --ignore-src -r -y
  ```
  
- check the serial port the EPMC module is connected to:
  > The best way to select the right serial port (if you are using multiple serial devices) is to select by path
  ```shell
  ls /dev/serial/by-path
  ```
  > You should see a value (if the driver is connected and seen by the computer), and your serial port would be -> /dev/serial/by-path/[value]. for more info visit this tutorial from [ArticulatedRobotics](https://www.youtube.com/watch?v=eJZXRncGaGM&list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&index=8)

  - OR you can also try this:
  ```shell
  ls /dev/ttyU*
  ```
  > you should see /dev/ttyUSB0 or /dev/ttyUSB1 and so on

- once you have gotten the **port**, update the **port** parameter in the **`<ros2_control>`** tag in the robot's URDF **`epmc_ros2_control.xacro`** file in the **`easy_demo_bot_description`** package, with the discovered port in the previous step

- Once that is done, do the same for the EIMU module and change the port parameter in the **`eimu_ros_start_params.yaml`** file found in the **`config`** folder of the **`easy_demo_bot_base`** package

- build the **epmc_hardware_interface** and **eimu_ros** packages with colcon (in your `ros workspace` root folder) (run in either PC or microcomputer like raspberry pi):
  ```shell
  colcon build --packages-select epmc_hardware_interface eimu_ros --symlink-install
  ```

#

#### Build the zed_bot packages
- In the `src/` folder of your `ros workspace`, clone the repo
  (or you can download and add it manually to the `src/` folder)
  ```shell
  git clone https://github.com/Oyefusi-Samuel/ZED-mobile-cleaning-simulated-robot..git zed_bot
  ```

- from the `src/` folder, cd into the root directory of your `ros workspace` and run rosdep to install all necessary ros dependencies
  ```shell
  cd ../
  rosdep install --from-paths src --ignore-src -r -y
  ```

- build the packages with colcon (in your `ros workspace` root folder) (run in either PC or microcomputer like raspberry pi):
  ```shell
  colcon build --packages-select zed_bot_description zed_bot_base --symlink-install
  ```
  
- only build the rviz package in a PC (not a microcomputer like raspberry pi):
  ```shell
  colcon build --packages-select zed_bot_rviz zed_bot_sim --symlink-install
  ```

#

### View Robot and Transform Tree

- open a new terminal and start the robot state publisher (where ever the EPMC and EIMU is - devPC or microcomputer)
  ```shell
  ros2 launch zed_bot_description rsp.launch.py use_joint_state_pub:=true
  ```
- in a differnt terminal on your Dev PC, run the rviz launch file to view the robot
  ```shell
  ros2 launch zed_bot_rviz rsp.launch.py
  ```
- To view transform tree, in a differnt terminal (while robot state publisher is still runing), run the following
  ```shell
  ros2 run rqt_tf_tree rqt_tf_tree
  ```

### Launch Robot Simulation

- close other terminal and launch this in a new terminal (in your Dev PC). don't forget to source your ros workspace
  ```shell
  ros2 launch zed_bot_sim sim.launch.py
  ```

#### Launch actual physical robot base without EKF (Default)
- by default the robot launch will be with the ekf using only the EPMC (i.e motor controller) module

- ensure the EPMC motor controller is connected serially.

- open a new terminal (on your Microcomputer - e.g. Raspberry Pi - or PC) and ensure you source your `ros workspace` in the terminal 

- start the robot base control
  ```shell
  ros2 launch zed_bot_base robot.launch.py
  ```
- open another terminal and ensure you source your `ros workspace` in the terminal

- launch the rviz (on your PC) to start robot base with odometry
  ```shell
  ros2 launch zed_bot_rviz robot.launch.py
  ```

#### Launch robot base with EKF
- ensure both the EPMC motor controller and the EIMU are connected serially.

- open the `robot.launch` file in the `zed_bot_base` package and change the **use_ekf** parameter to 'True'. this will start the EIMU and EKF node alongside the EPMC ros2 control
```
declare_use_ekf_cmd = DeclareLaunchArgument(
      name='use_ekf',
      default_value='True', 
      description='fuse odometry and imu data if true')
```

- open a new terminal and ensure you source your `ros workspace` in the terminal

- start the robot base control
  ```shell
  ros2 launch zed_bot_base robot.launch.py
  ```
- open another terminal and ensure you source your `ros workspace` in the terminal

- launch the rviz to display robot base with filterd odometry 
  ```shell
  ros2 launch zed_bot_rviz robot.launch.py
#

#### DRIVING / CONTROL
- you can now drive the **zed_bot** with the default ROS teleop package

- But I recommend driving the **zed_bot** with the [**arrow_key_teleop_drive**](https://github.com/samuko-things/arrow_key_teleop_drive) package I created to make driving robot easy using just your keyboard arrow keys.

- if you,ve downloaded and build the **arrow_key_teleop_drive**, run this command to drive the robot. don't forget to source your workspace.
  ```shell
  ros2 run arrow_key_teleop_drive arrow_key_teleop_drive
  ```
  OR
  ```shell
  ros2 run arrow_key_teleop_drive arrow_key_teleop_drive <v in m/s> <w in rad/sec>
  ```
