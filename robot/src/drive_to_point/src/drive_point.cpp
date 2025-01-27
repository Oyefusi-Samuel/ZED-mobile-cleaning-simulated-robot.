#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"

class Following_waypoints : public rclcpp::Node {
public:
  Following_waypoints(): Node("waypoint_follower"), current_waypoint_idx_(0) {

    // Create a subscriber to receive the robot's odometry
    subscriber_ = this->create_subscription<nav_msgs::msg::Odometry>("/odom", 10,std::bind(&Following_waypoints::odomCallback, this, std::placeholders::_1));

    // Create a publisher to send velocity commands to the robot
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

    // Define the waypoints
    defineWaypoints();
  }

private:
  void odomCallback(const nav_msgs::msg::Odometry::SharedPtr msg) {
    // Check if the robot has reached the current waypoint
    double distance = computeDistance(msg->pose.pose, waypoints_[current_waypoint_idx_].pose);
    if (distance < 0.1) {
      // Move to the next waypoint
      current_waypoint_idx_++;
      if (current_waypoint_idx_ >= waypoints_.size()) {
        RCLCPP_INFO(this->get_logger(), "Robot reached all waypoints!");
        // Stop the robot
        geometry_msgs::msg::Twist stop_cmd;
        publisher_->publish(stop_cmd);
        return;
      }
    }

    // Compute the desired velocity command to move towards the current waypoint
    geometry_msgs::msg::Twist velocity_cmd;
    velocity_cmd.linear.x = 0.2;  // Forward linear velocity
    velocity_cmd.angular.z = calculateAngularVelocity(msg->pose.pose, waypoints_[current_waypoint_idx_].pose);
    publisher_->publish(velocity_cmd);
  }

  double computeDistance(const geometry_msgs::msg::Pose& pose1, const geometry_msgs::msg::Pose& pose2) {
    double dx = pose2.position.x - pose1.position.x;
    double dy = pose2.position.y - pose1.position.y;
    return std::hypot(dx, dy);
  }

  double calculateAngularVelocity(const geometry_msgs::msg::Pose& current_pose,const geometry_msgs::msg::Pose& target_pose) {
    // Calculate the desired angular velocity to rotate towards the target pose
    double dx = target_pose.position.x - current_pose.position.x;
    double dy = target_pose.position.y - current_pose.position.y;
    return std::atan2(dy, dx);
  }

  void defineWaypoints() {
    // Define the desired waypoints here
    // Each waypoint should have a position (x, y, z) and an orientation (quaternion or Euler angles)
    geometry_msgs::msg::PoseStamped waypoint1;
    waypoint1.pose.position.x = 0.1;
    waypoint1.pose.position.y = 0.2;
    waypoint1.pose.position.z = 0.0;
    waypoint1.pose.orientation.w = 1.0;
    waypoints_.push_back(waypoint1);

    geometry_msgs::msg::PoseStamped waypoint3;
    waypoint3.pose.position.x = 0.3;
    waypoint3.pose.position.y = 0.4;
    waypoint3.pose.position.z = 0.0;
    waypoint3.pose.orientation.w = 1.0;
    waypoints_.push_back(waypoint3);

  }

  std::vector<geometry_msgs::msg::PoseStamped> waypoints_;
  size_t current_waypoint_idx_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscriber_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<Following_waypoints>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
