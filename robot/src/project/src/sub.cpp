#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using std::placeholders::_1;

class subscriber : public rclcpp::Node{
public:
     subscriber() : Node("velocity_sub"){
        sub = this->create_subscription<geometry_msgs::msg::Twist>("/cmd_vel",1,std::bind(&subscriber::subscriber_message,this,_1));
    }
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr sub;

private:
     void subscriber_message(const geometry_msgs::msg::Twist::SharedPtr msg)const{
        RCLCPP_INFO(this->get_logger(),"The veloicty_messsage_reading: %f",msg->linear.x,msg->angular.z);
    }
};

int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<subscriber>());
    rclcpp::shutdown();
    return 0;
}