cmake_minimum_required(VERSION 3.5)
project(project)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

#########################################################
#Add this files
# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(project src/pub.cpp)
add_executable(move src/drive_straight.cpp)
add_executable(sub src/sub.cpp)
add_executable(avoid_obstacle src/avoid_obstacle.cpp)


ament_target_dependencies(project rclcpp geometry_msgs)
ament_target_dependencies(move rclcpp geometry_msgs)
ament_target_dependencies(sub rclcpp geometry_msgs)
ament_target_dependencies(avoid_obstacle rclcpp geometry_msgs)


install(TARGETS
    project
    move
    sub
    avoid_obstacle
    DESTINATION lib/${PROJECT_NAME}
)
####################################################


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
