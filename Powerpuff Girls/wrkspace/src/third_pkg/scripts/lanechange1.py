#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import tf.transformations
import time

# Global variables
i = -100
j = -100
desired_angle = 0
start_time = time.time()

# Callback function to handle odometry messages
def call(msg):
    global j, i, desired_angle
    i = msg.pose.pose.position.x
    j = msg.pose.pose.position.y

    # Extract the orientation quaternion
    orientation_quat = msg.pose.pose.orientation

    # Convert the quaternion to Euler angles (roll, pitch, yaw)
    (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([
        orientation_quat.x, orientation_quat.y, orientation_quat.z, orientation_quat.w])

    # Extract the desired angle (yaw)
    desired_angle = yaw
    rospy.loginfo(f"Current position: x={i}, y={j}")

def walk():
    global i, j, desired_angle

    # Initialize publishers
    pub_vel = rospy.Publisher("cmd_vel", Float64, queue_size=10)
    pub_brakes = rospy.Publisher("brakes", Float64, queue_size=10)
    pub_steer = rospy.Publisher("SteeringAngle", Float64, queue_size=10)

    # Initialize the node
    rospy.init_node("walker", anonymous=True)

    # Subscribe to the odometry topic
    rospy.Subscriber('odom', Odometry, call)

    # Set rate
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # Check the y position
        if j >= -10:
            if i > -3.7:
                # Continue moving forward
                rospy.loginfo("Moving forward")
                pub_steer.publish(10)  # Adjust as needed
                pub_vel.publish(0.1)
            else:
                # Check the desired angle
                if desired_angle > 0:
                    rospy.loginfo("Turning left")
                    pub_steer.publish(-8.5)  # Turn left
                else:
                    rospy.loginfo("Straightening")
                    pub_steer.publish(0)  # Straighten the steering

                if j >= 60:
                    rospy.loginfo("Approaching end of lane, stopping and braking")
                    pub_vel.publish(0)  # Stop the vehicle
                    for brake_value in range(0, 11):  # Gradual braking
                        pub_brakes.publish(brake_value / 10.0)
                        rospy.sleep(0.1)
                else:
                    rospy.loginfo("Moving forward")
                    pub_vel.publish(0.1)
                    pub_brakes.publish(0)  # No brakes

        else:
            rospy.loginfo("Moving forward")
            pub_vel.publish(0.1)
            pub_brakes.publish(0)  # No brakes

        # Sleep to maintain loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        walk()
    except rospy.ROSInterruptException:
        pass
