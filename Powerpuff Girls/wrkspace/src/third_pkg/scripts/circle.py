#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import numpy as np
import time


start=time.time()
i=-100
j=-100

#callback function
def call(msg):
    global j,i
    i=msg.pose.pose.position.x
    #get y from msg
    j=msg.pose.pose.position.y
    rospy.loginfo(j)
    plt.plot(i,j,marker=('o') ,markersize=10, linestyle='None', color='red')
    plt.axis('equal')
    plt.draw()
    plt.pause(0.01)


#main function
def walk():
    global j
    #make pubisher
    pub1=rospy.Publisher("cmd_vel",Float64,queue_size=10)
    # pub2=rospy.Publisher("brakes",Float64,queue_size=10)
    pub3=rospy.Publisher("SteeringAngle",Float64,queue_size=10)
    #make a subscriber
    rospy.Subscriber('odom',Odometry,call) #topic should match that in coppeliaSim
    #make node
    rospy.init_node("walker",anonymous=True)
    #set rate
    rate=rospy.Rate(10) #in HZ
    #write & publish string
    while not rospy.is_shutdown():
        end=time.time()
        msg= 20.71         #steering_angle = atan(wheelbase / turning_radius)
        rospy.loginfo(msg)
        pub3.publish(msg)
        msg= 0.1           #had to slow it down to prevent skidding
        rospy.loginfo(msg)
        pub1.publish(msg)
        #sleep
        rate.sleep()
        #spin
        # rospy.spin()



#function call with exception check
if __name__=='__main__':
    try:
            walk()
    except rospy.ROSInterruptException:
        pass 
