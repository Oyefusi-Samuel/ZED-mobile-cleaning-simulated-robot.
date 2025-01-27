cmake_minimum_required(VERSION 3.5)
project(drive_to_point)

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

######################################################
# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)


add_executable(drive_to_point src/drive_point.cpp)  
add_executable(amclpose src/amcl_pose.cpp) 
ament_target_dependencies(drive_to_point rclcpp geometry_msgs nav_msgs)
ament_target_dependencies(amclpose rclcpp geometry_msgs nav_msgs)


install(TARGETS
    drive_to_point
    amclpose
    DESTINATION lib/${PROJECT_NAME}
)

########################################################
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
