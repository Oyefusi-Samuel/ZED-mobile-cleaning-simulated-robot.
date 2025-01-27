#pragma once 
#include "sensor_msgs/msg/laser_scan.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

namespace bump_{
    using namespace std::chrono_literals;
class bump : public rclcpp::Node{
    public:
        bump(); //default constructor class
        
    private:
        void laser_callback(const sensor_msgs::msg::LaserScan::UniquePtr msg);//laser_scan callback 
        void control_cycle();
        int state;
        rclcpp::Time state_ts;
        void foward();
        //Time duration
        const rclcpp::Duration Turning_time {2s};
        const rclcpp::Duration Backward_time{2s};
        const rclcpp::Duration Scan_time{1s};

        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub;
        rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub;
        rclcpp::TimerBase::SharedPtr timer_;
        sensor_msgs::msg::LaserScan::UniquePtr last_scan;
};

}//namespace bump_go_cpp

