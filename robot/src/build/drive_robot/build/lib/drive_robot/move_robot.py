import rclpy #import the rclpy library.
from geometry_msgs.msg import Twist #import the geometry_msgs package.
from rclpy.node import Node

#Create a class that contains the execution.
class Move(Node):
    def __init__(self):
        super().__init__("move_robot") #Initilizing the Node.
        self.pub = self.create_publisher(Twist,"/cmd_vel",1000) #An object called pub that stores the command velocity topic called "/cmd_vel" in this case.
        self.velocity_message = Twist() #storing the type called Twist.
        self.msg = "The robot is driving forward" #storing the string message.
        self.time = 0.05 
        self.timer = self.create_timer(self.time,self.velocity_direction)

    #Create a method called velocity_direction that stores the direction of the robot.
    def velocity_direction(self):
        #We want our robot to drive forward.
        self.velocity_message.linear.x = 0.2 #Robot drives 0.2 m/s in the x direction forward.
        self.pub.publish(self.velocity_message) #Publish to the wheels of the robot.
        print(self.msg) #Print the robot is driving forward.


#The main function that calls the class name.
def main(args=None):
    rclpy.init(args=args)
    move = Move() #Saving the class name into a variable.
    move.velocity_direction()
    rclpy.spin(move) #We want the node to keep running.
    #rclpy.shutdown() #shutdown the script/Node once the ctrl + c key is being pressed.

if __name__ == '__main__':
    main() #Calling the main function.




