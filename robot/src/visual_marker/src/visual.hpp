#pragma once 
#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "visualization_msgs/msg/marker.hpp"
#include "tf2_ros/static_transform_broadcaster.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "rclcpp/duration.hpp"
// #include "tf2_"


namespace visual_marker{
    using namespace std::chrono_literals;
    class visual : public rclcpp::Node{
        public:
            visual();
            void laser_callback(sensor_msgs::msg::LaserScan::SharedPtr msg);
            void control_cycle();
            const int distance_from_obstacle = 1;
            // float distance;
            float speed;
            double laser_scan;
            // double distance;
            rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub;
            rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr marker;
            rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub;
            rclcpp::TimerBase::SharedPtr timer_;
            //sensor_msgs::msg::LaserScan::UniquePtr last_scan;
            // tf2_ros::TransformBroadcaster broadcast_transforms;
            // geometry_msgs::msg::TransformStamped stamped_transform;
            tf2_ros::StaticTransformBroadcaster  tf_broadcaster_;
            tf2_ros::Buffer buffer_transform;
            // tf2_ros::TransformListener listener(buffer_transform);
            visualization_msgs::msg::Marker mark;
            sensor_msgs::msg::LaserScan::UniquePtr distance;
            geometry_msgs::msg::Point point_start,end;
            float threshold = 2.0;
            
        };


}//namspace visual_marker