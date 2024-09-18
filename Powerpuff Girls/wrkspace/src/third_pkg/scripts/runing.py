#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
#from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import math

previous_y = None
total_distance_y = 0.0
distance_target = 46.5 # Target distance in meters i have decreesed the value because the brakes take time to fully stop the vehcle
msg_brakes=0
msg_vel = 0.5



def odom_callback(data):
    global previous_y, total_distance_y, distance_target,msg_brakes,msg_vel
    pup_brakes= rospy.Publisher('brakes',Float64,queue_size=10)

    # Extract the current y position from the odometry message
    current_y = data.pose.pose.position.y

    if previous_y is not None:
        # Calculate the distance traveled along the y-axis since the last position
        distance_y = abs(current_y - previous_y)
        
        # Update the total distance traveled along the y-axis
        total_distance_y += distance_y
        
        # Log the total distance traveled along the y-axis
        rospy.loginfo(f"Total distance traveled along y-axis: {total_distance_y:.2f} meters")
        
        # Check if the robot has reached or exceeded the target distance
        if total_distance_y >= distance_target:
            rospy.loginfo("Target distance of 75 meters along y-axis reached!")
            msg_brakes=1
            rospy.loginfo(msg_brakes)
            pup_brakes.publish(msg_brakes)
            msg_vel = 0
            
    
    # Update the previous_y for the next callback
    previous_y = current_y

def runner():
    
    pup_vel= rospy.Publisher('cmd_vel',Float64,queue_size=10)
    pup_steer= rospy.Publisher('SteeringAngle',Float64,queue_size=10)
    
    rospy.init_node('runner',anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown():
        rospy.Subscriber('/odom', Odometry, odom_callback)
        
        msg_steer=0
        rospy.loginfo(msg_vel)
        pup_vel.publish(msg_vel)
        rospy.loginfo(msg_steer)
        pup_steer.publish(msg_steer)
        rate.sleep()
        





if __name__ == '__main__':
    try:
      runner()
    except rospy.ROSInterruptException:
        pass  
