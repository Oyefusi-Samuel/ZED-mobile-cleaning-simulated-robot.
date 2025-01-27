#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <cmath>
using std::cin;
using std::cout;


using namespace std::chrono_literals;

class Movement : public rclcpp::Node{
public: 
     Movement() : Node("movement_direction"){
        command_velocity_pub = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel",10);
        timer_ = this->create_wall_timer(500ms,std::bind(&Movement::velocity_movement,this));
     }
    //declare the pointer to the command_velocity_pub 
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr command_velocity_pub;
    float i;
private:
    void velocity_movement(){
        auto store_vel = geometry_msgs::msg::Twist();
        store_vel.linear.x = 0.2;
        store_vel.angular.z = M_1_PI/2;
        command_velocity_pub->publish(store_vel);
    }
};


int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Movement>());
    rclcpp::shutdown();
    return 0;
}