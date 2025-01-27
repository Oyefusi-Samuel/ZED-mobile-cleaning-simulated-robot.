#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
using namespace std::chrono_literals;
using std::placeholders::_1;


class avoid_obstacle : public rclcpp::Node{
    public: 
        avoid_obstacle() : Node("avoid_obstacle"){
            command_vel_pub =this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel",10);
            laser_sub = this->create_subscription<sensor_msgs::msg::LaserScan>("/scan",1,std::bind(&avoid_obstacle::laser_callback,this,_1));
        }
        void drive_right(){
            auto move_robot = geometry_msgs::msg::Twist();
            move_robot.angular.z = speed;
            command_vel_pub->publish(move_robot);
            RCLCPP_INFO(this->get_logger(),"The robot drives right");
        }
        void drive_left(){
            auto move_robot = geometry_msgs::msg::Twist();
            move_robot.angular.z = -speed;
            command_vel_pub->publish(move_robot);
        }
        void stop(){
            auto move_robot = geometry_msgs::msg::Twist();
            move_robot.linear.x = 0.0;
            move_robot.linear.z = 0.0;
            command_vel_pub->publish(move_robot);
        }
  private:
       void laser_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg){
            geometry_msgs::msg::Twist command_vel;
            if (msg->ranges[msg->ranges.size()/2] < 2){
                command_vel.linear.x = 0.0;
            }
            else{
                command_vel.linear.x = speed;
            }
            command_vel_pub->publish(command_vel);
        }
        float speed = 0.2;
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr command_vel_pub;
        rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr laser_sub;
};//class avoid_obstacle


int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    // auto node = std::make_shared<avoid_obstacle>();
    rclcpp::spin(std::make_shared<avoid_obstacle>());
    // rclcpp::spin(node);
    rclcpp::shutdown();
}