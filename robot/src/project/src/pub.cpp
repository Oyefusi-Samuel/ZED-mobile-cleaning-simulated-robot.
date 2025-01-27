#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <iostream>
using namespace std::chrono_literals;

class move : public rclcpp::Node {
public:
     move() :Node("movement"){
        publisher  = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel",10);
        timer_ = this->create_wall_timer(500ms,std::bind(&move::velocity_movement,this));
     }
//this message type cannot be operated in the same constructor you are working with
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher;
    float i;
private:
    //make the robot do_something method
    void velocity_movement(){
        auto velocity_message = geometry_msgs::msg::Twist();
        //drive robot forward
        velocity_message.linear.x = 0.2 + i; //increment the speed by 0.1
        velocity_message.angular.z = 0.2;
        publisher->publish(velocity_message);
        i +=0.1;
    }

};


int main(int argc, char**argv){
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<move>());
    rclcpp::shutdown();
    return 0;
}