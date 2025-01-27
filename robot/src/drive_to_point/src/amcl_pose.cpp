#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
#include <chrono>
#include <memory>

using namespace std::chrono_literals;

class PoseEstimate : public rclcpp::Node {
public:
    PoseEstimate() : Node("pose_estimate") {
        pose_pub = this->create_publisher<geometry_msgs::msg::PoseWithCovarianceStamped>("/amcl_pose", 10);
        timer_ = this->create_wall_timer(500ms, std::bind(&PoseEstimate::controlCycle, this));
        RCLCPP_INFO(this->get_logger(), "The node just started");
    }

private:
    void controlCycle() {
        pose_.header.frame_id = "/map";
        pose_.header.stamp = this->now();
        pose_.pose.pose.position.x = 0.0;
        pose_.pose.pose.position.y = 0.0;
        pose_.pose.pose.orientation.z = 0.0;
        pose_.pose.pose.orientation.w = 0.2;
        pose_pub->publish(pose_);
    }

    rclcpp::Publisher<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr pose_pub;
    geometry_msgs::msg::PoseWithCovarianceStamped pose_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PoseEstimate>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
