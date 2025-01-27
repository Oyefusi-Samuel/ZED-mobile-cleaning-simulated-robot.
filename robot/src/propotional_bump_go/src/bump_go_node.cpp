#include <utility>
#include "bump_go.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "geometry_msgs/msg/twist.hpp"

namespace bump_
{   
    using namespace std::chrono_literals;
    using std::placeholders::_1;
    
    bump::bump() :Node("bump_go_node"){
            scan_sub = this->create_subscription<sensor_msgs::msg::LaserScan>("/scan",1,std::bind(&bump::laser_callback,this,_1));
            vel_pub = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel",10);
            timer_ = this->create_wall_timer(50ms,std::bind(&bump::control_cycle,this));
            state_ts = now();
    }//constructor bump_go

            rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub;
            rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub;
            rclcpp::TimerBase::SharedPtr timer_;
            float forward_speed = 0.2;
            float distance_laser;

    void stop(){
            geometry_msgs::msg::Twist command_vel;
            command_vel.linear.x = 0.0;
            vel_pub->publish(command_vel);
    }

    void forward(){
            geometry_msgs::msg::Twist command_vel;
            command_vel.linear.x = forward_speed;
            vel_pub->publish(command_vel);
    }  

    //laser_callback
    void bump::laser_callback(const sensor_msgs::msg::LaserScan::UniquePtr msg){ 
            distance_laser = msg->ranges[msg->ranges.size()/2];
    }//laser scan callback
    //The motion function

    void bump::control_cycle(){
            std::cout<<"The node is activated" << std::endl;
            geometry_msgs::msg::Twist command_vel;
            command_vel.linear.x = forward_speed;
            vel_pub->publish(command_vel);
            if (distance_laser < 2){
                command_vel.angular.z = 0.2;
                vel_pub->publish(command_vel);
            }
            else if (distance_laser == 2){
                command_vel.linear.x = 0.0;
                command_vel.angular.z = 0.0;
                vel_pub->publish(command_vel);
            }
            if (!std::isinf(distance_laser)){ //! infinity(when obstacle detected)
                geometry_msgs::msg::Twist command_vel;
                command_vel.angular.z = -0.2;
                vel_pub->publish(command_vel);
            }
        }

} // namespace bump_go_cpp

int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<bump_::bump>();
    rclcpp::spin(node);
    return 0;
}