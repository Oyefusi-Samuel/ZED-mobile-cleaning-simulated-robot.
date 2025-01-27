#include <utility>
#include "visual.hpp"
#include "rclcpp/duration.hpp"

namespace  visual_marker{
    using std::placeholders::_1;
        visual::visual() : Node("Visual_markers_node")
        {
            vel_pub = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel",10);
            scan_sub = this->create_subscription<sensor_msgs::msg::LaserScan>("/scan",10,std::bind(&visual::laser_callback,this,_1));
            marker = this->create_publisher<visualization_msgs::msg::Marker>("/Rviz_marker",10);
            timer_ =this->create_wall_timer(50ms,std::bind(&visual::control_cycle,this));
            tf_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(*this);
        }
    void visual::laser_callback(sensor_msgs::msg::LaserScan::SharedPtr msg){
        double distance = msg->ranges[msg->ranges.size()/2];
        if (!std::isinf(distance)){ //if object detected
            geometry_msgs::msg::TransformStamped stamped_transform;
            stamped_transform.header = msg->header;
            stamped_transform.header.stamp = now();
            stamped_transform.header.frame_id = "base_link";
            stamped_transform.child_frame_id = "obstacle_dectected";//base frame of the robot
            stamped_transform.transform.translation.x = 0.0;
            tf_broadcaster_ = buffer_transform.lookupTransform("base_link","obstale_detected",tf2::TimePointZero);
            tf_broadcaster_.sendTransform(stamped_transform);
        }
    }
    float speed = 0.2;
    //main cycle
    void visual::control_cycle(){
        geometry_msgs::msg::Twist velocity_pub;
        velocity_pub.linear.x = speed;
        vel_pub->publish(velocity_pub);
        if (distance){ //obstacle detected
           mark.header.frame_id = "base_link"; //center of the robot
           mark.header.stamp = now();
           mark.type = visualization_msgs::msg::Marker::ARROW;//set the marker arrow 
           mark.type = visualization_msgs::msg::Marker::ADD;
           mark.lifetime =rclcpp::Duration(5s);
        
           //Arrow marker points
           point_start.x = 0.0;
           point_start.y =0.0;
           point_start.z = 0.0;

           //marker arrow color
           mark.color.r = 1.0;
           mark.color.g = 0.0;
           mark.color.b = 0.0;
           mark.color.a = 1.0;//set this to 1 so the arrow gets visible

           //marker arrow size
           mark.scale.x = 0.02;
           mark.scale.y = 0.1;
           mark.scale.z = 0.1;

           marker->publish(mark);
        }

        else {
           return;
        }
    }
}//namespace visual_marker

int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<visual_marker::visual>());
    return 0;
}